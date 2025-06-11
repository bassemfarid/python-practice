#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#ifdef WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <sys/wait.h>
#endif
#include "constants.h"
#include "error.h"
#include "programHandler.h"

char* programHandler_GetProgramName(char* programNumber) {
    int numbers[3];
    if(sscanf(programNumber, "%d-%d-%d", &numbers[0], &numbers[1], &numbers[2]) != 3)
        error("Invalid program number: %s\n", programNumber);
    
    // Get the name of the program 
    char raw[MAX_PROGRAM_PATH_SIZE];
    if(!raw) error("Failed to create a buffer to store the program path\n");
    snprintf(raw, MAX_PROGRAM_PATH_SIZE,
             "%s/tests/%02d-%02d-%02d/generator.py",
             BASE_PATH, numbers[0], numbers[1], numbers[2]);

    FILE* generator = fopen(raw, "r");
    if(!generator) error("Failed to find the generator at %s\n", raw);
    fclose(generator);
    
    // Condense the memory used
    char* ret = calloc(strlen(raw)+1, 1);
    if(!ret) error("Failed to create a buffer to store the program path\n");
    strcpy(ret, raw);

    return ret;
}

#ifdef WIN32
void programHandler_ReadAvailableOutput(HANDLE hOutput, char **outputBuffer, unsigned *currentSize) {
    DWORD availableBytes = 0;
    char tempBuffer[256];
    DWORD bytesRead;

    while(PeekNamedPipe(hOutput, NULL, 0, NULL, &availableBytes, NULL) && availableBytes > 0) {
        if(ReadFile(hOutput, tempBuffer, sizeof(tempBuffer) - 1, &bytesRead, NULL) && bytesRead > 0) {
            tempBuffer[bytesRead] = 0;

            size_t newSize = *currentSize + bytesRead + 1;
            if(newSize >= PROGRAMIO_INITIAL_SIZE) {
                char *temp = realloc(*outputBuffer, newSize);
                if(!temp) error("Failed to reallocate output buffer");
                *outputBuffer = temp;
            }

            strcat(*outputBuffer, tempBuffer);
            *currentSize += bytesRead;
        } else break;
    }
}

int programHandler_ProcessHasExited(HANDLE processHandle) {
    DWORD exitCode = 0;
    if(!GetExitCodeProcess(processHandle, &exitCode))
        error("Failed to get process exit code");
    return exitCode != STILL_ACTIVE;
}


char** programHandler_RunPythonProgram(char* path) {
    HANDLE hChildStdoutRd = NULL, hChildStdoutWr = NULL;
    HANDLE hChildStdinRd = NULL, hChildStdinWr = NULL;
    SECURITY_ATTRIBUTES saAttr = {0};
    PROCESS_INFORMATION piProcInfo = {0};
    STARTUPINFO siStartInfo = {0};
    char **programIO = calloc(2, sizeof(char*));
    if(!programIO) error("Failed to allocate memory for program IO");

    programIO[0] = calloc(PROGRAMIO_INITIAL_SIZE, 1);
    programIO[1] = calloc(PROGRAMIO_INITIAL_SIZE, 1);
    if(!programIO[0] || !programIO[1]) {
        free(programIO);
        error("Failed to allocate input/output buffer");
    }

    saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
    saAttr.bInheritHandle = 1;
    saAttr.lpSecurityDescriptor = NULL;

    if(!CreatePipe(&hChildStdoutRd, &hChildStdoutWr, &saAttr, 0)) {
        free(programIO[0]);
        free(programIO[1]);
        free(programIO);
        error("Stdout pipe creation failed");
    }

    if(!CreatePipe(&hChildStdinRd, &hChildStdinWr, &saAttr, 0)) {
        free(programIO[0]);
        free(programIO[1]);
        free(programIO);
        error("Stdin pipe creation failed");
    }

    if(!SetHandleInformation(hChildStdoutRd, HANDLE_FLAG_INHERIT, 0)) {
        free(programIO[0]);
        free(programIO[1]);
        free(programIO);
        error("SetHandleInformation failed");
    }

    siStartInfo.cb = sizeof(STARTUPINFO);
    siStartInfo.hStdError = hChildStdoutWr;
    siStartInfo.hStdOutput = hChildStdoutWr;
    siStartInfo.hStdInput = hChildStdinRd;
    siStartInfo.dwFlags |= STARTF_USESTDHANDLES;

    char processCommand[MAX_PROGRAM_PATH_SIZE + 20];
    if(snprintf(processCommand, sizeof(processCommand), "python -u \"%s\"", path) >= sizeof(processCommand)) {
        free(programIO[0]);
        free(programIO[1]);
        free(programIO);
        error("Python path too long");
    }

    if(!CreateProcess(NULL, processCommand, NULL, NULL, 1, 0, NULL, NULL, &siStartInfo, &piProcInfo)) {
        free(programIO[0]);
        free(programIO[1]);
        free(programIO);
        error("CreateProcess failed");
    }

    // Close unused handles
    CloseHandle(hChildStdoutWr);
    CloseHandle(hChildStdinRd);
    
    // Give python some time to crash if the program raises an error
    Sleep(OUTPUT_DELAY);

    // If it didn't crash, print the input prompt
    if(!programHandler_ProcessHasExited(piProcInfo.hProcess))
        printf("Case generator started. Input below:\n");

    char inputBuffer[INPUT_BUFFER_SIZE];
    DWORD bytesWritten;
    unsigned inputSize = 0;
    unsigned outputSize = 0;

    while(!programHandler_ProcessHasExited(piProcInfo.hProcess)) {
        if(fgets(inputBuffer, INPUT_BUFFER_SIZE, stdin)) {
            unsigned len = strlen(inputBuffer);

            unsigned newInputSize = inputSize + len + 1;
            if(newInputSize >= PROGRAMIO_INITIAL_SIZE) {
                char *tempInput = realloc(programIO[0], newInputSize);
                if(!tempInput) {
                    free(programIO[0]);
                    free(programIO[1]);
                    free(programIO);
                    error("Failed to reallocate input buffer");
                }
                programIO[0] = tempInput;
            }

            strcat(programIO[0], inputBuffer);
            inputSize += len;

            if(!WriteFile(hChildStdinWr, inputBuffer, (DWORD)len, &bytesWritten, NULL)) {
                free(programIO[0]);
                free(programIO[1]);
                free(programIO);
                error("Failed to write to stdin pipe");
            }

            // After writing input, read any available output
            programHandler_ReadAvailableOutput(hChildStdoutRd, &programIO[1], &outputSize);
        }

        // Also poll output while waiting for next input
        programHandler_ReadAvailableOutput(hChildStdoutRd, &programIO[1], &outputSize);
        Sleep(OUTPUT_DELAY);
    }

    // Final read to collect remaining output
    programHandler_ReadAvailableOutput(hChildStdoutRd, &programIO[1], &outputSize);

    // Check that the program exited correctly (exit code 0)
    DWORD exitCode = 1;
    if(!GetExitCodeProcess(piProcInfo.hProcess, &exitCode)) {
        free(programIO[0]);
        free(programIO[1]);
        free(programIO);
        error("Failed to get process exit code");
    }
    if(exitCode)
        error("Python exited with code %u. Full output:\n%s", exitCode, programIO[1]); // Leaks memory, but I don't care, I'd rather the logs

    CloseHandle(hChildStdinWr);
    CloseHandle(hChildStdoutRd);
    WaitForSingleObject(piProcInfo.hProcess, INFINITE);
    CloseHandle(piProcInfo.hProcess);
    CloseHandle(piProcInfo.hThread);

    return programIO;
}
#else
char** programHandler_RunPythonProgram(char* path) {
    int inPipe[2], outPipe[2];
    pid_t pid;
    char** programIO = calloc(2, sizeof(char*));

    if(!programIO) error("Failed to allocate memory for program IO");
    programIO[0] = calloc(PROGRAMIO_INITIAL_SIZE, 1);
    programIO[1] = calloc(PROGRAMIO_INITIAL_SIZE, 1);
    if(!programIO[0] || !programIO[1]) error("Failed to allocate input/output buffer");

    if(pipe(inPipe) == -1 || pipe(outPipe) == -1)
        error("Pipe creation failed");

    if((pid = fork()) == -1)
        error("Fork failed");

    if(!pid) {
        // Redirect stdio and stdout
        dup2(inPipe[0], STDIN_FILENO);
        dup2(outPipe[1], STDOUT_FILENO);
        close(inPipe[0]);
        close(inPipe[1]);
        close(outPipe[0]);
        close(outPipe[1]);

        execlp("python3", "python3", "-u", path, NULL);
        error("Failed to exec Python");
    } else {
        close(inPipe[0]);
        close(outPipe[1]);

        fcntl(outPipe[0], F_SETFL, O_NONBLOCK);

        // Handle IO
        char inputBuffer[INPUT_BUFFER_SIZE];
        int inputSize = 0;
        while(1) {
            if(fgets(inputBuffer, INPUT_BUFFER_SIZE, stdin)) {
                int len = strlen(inputBuffer);

                // Store input dynamically
                if(inputSize + len >= PROGRAMIO_INITIAL_SIZE) {
                    programIO[0] = realloc(programIO[0], inputSize + len + 1);
                    if(!programIO[0]) error("Failed to reallocate input buffer");
                }

                strcat(programIO[0], inputBuffer);
                inputSize += len;

                // Write input to Python process
                write(inPipe[1], inputBuffer, len);
            }

            // Check if Python has produced output
            usleep(OUTPUT_DELAY * 1000);
            char buffer[256];
            int bytesRead = read(outPipe[0], buffer, sizeof(buffer) - 1);

            if(bytesRead > 0) {
                buffer[bytesRead] = 0;

                // Store output dynamically
                size_t totalSize = strlen(programIO[1]);
                programIO[1] = realloc(programIO[1], totalSize + bytesRead + 1);
                if (!programIO[1]) error("Failed to reallocate output buffer");

                strcat(programIO[1], buffer);
                break;
            }
        }
        close(inPipe[1]);

        // Read remaining output from Python
        char buffer[256];
        ssize_t bytesRead;
        while((bytesRead = read(outPipe[0], buffer, sizeof(buffer) - 1)) > 0) {
            buffer[bytesRead] = 0;

            // Store output dynamically
            size_t totalSize = strlen(programIO[1]);
            programIO[1] = realloc(programIO[1], totalSize + bytesRead + 1);
            if (!programIO[1]) error("Failed to reallocate output buffer");

            strcat(programIO[1], buffer);
        }

        close(outPipe[0]);
        waitpid(pid, NULL, 0);
    }
    return programIO;
}
#endif