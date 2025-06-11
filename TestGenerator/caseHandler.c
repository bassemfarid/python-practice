#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "constants.h"
#include "error.h"
#include "caseHandler.h"

int caseHandler_GetNextCase(char* programNumber) {
    int numbers[3];
    if(sscanf(programNumber, "%d-%d-%d", &numbers[0], &numbers[1], &numbers[2]) != 3)
        error("Invalid program number: %s\n", programNumber);
    
    // Get the name of the directory
    char dirName[MAX_PROGRAM_PATH_SIZE];
    snprintf(dirName, MAX_PROGRAM_PATH_SIZE, "%s/tests/%02d-%02d-%02d/",
                                             BASE_PATH, numbers[0], numbers[1], numbers[2]);
    
    // Find what the first unwritten test number is
    int number = 1;
    char testName[MAX_PROGRAM_PATH_SIZE+10];
    while(1) {
        snprintf(testName, MAX_PROGRAM_PATH_SIZE+10, "%s1-%02d.in", dirName, number);
        FILE* file = fopen(testName, "r");
        if(file) {
            fclose(file);
            number++;
            continue;
        }
        break;
    }

    return number;
}

void caseHandler_PopulateNextCase(char* programNumber, int caseNumber, char** programIO) {
    int numbers[3];
    if(sscanf(programNumber, "%d-%d-%d", &numbers[0], &numbers[1], &numbers[2]) != 3)
        error("Invalid program number: %s\n", programNumber);

    // Open up the input and output files
    char inFileName[MAX_PROGRAM_PATH_SIZE], outFileName[MAX_PROGRAM_PATH_SIZE];
    snprintf(inFileName,  MAX_PROGRAM_PATH_SIZE, "%s/tests/%02d-%02d-%02d/1-%02d.in",
                                                 BASE_PATH, numbers[0], numbers[1], numbers[2], caseNumber);
    snprintf(outFileName, MAX_PROGRAM_PATH_SIZE, "%s/tests/%02d-%02d-%02d/1-%02d.out",
                                                 BASE_PATH, numbers[0], numbers[1], numbers[2], caseNumber);
    FILE* inFile  = fopen(inFileName, "w");
    if(!inFile) error("Failed to write to .in file\n");
    FILE* outFile = fopen(outFileName, "w");
    if(!outFile) error("Failed to write to .out file\n");

    // Turn all "\r\n" occurrences in the output into just '\n'
    char* newOutput = calloc(strlen(programIO[1])+1, 1);
    if(!newOutput) error("Failed to allocate new output buffer\n");
    int i = 0, index = 0;
    while(programIO[1][i]) {
        if(programIO[1][i] == '\r' && programIO[1][i+1] == '\n') {
            newOutput[index++] = '\n';
            i += 2;
        } else newOutput[index++] = programIO[1][i++];
    }
    free(programIO[1]);
    programIO[1] = newOutput;

    // Strip the '\n' at the end of the input and output
    programIO[0][strlen(programIO[0])-1] = 0;
    programIO[1][strlen(programIO[1])-1] = 0;

    // Write the input and output from programIO to the files
    fwrite(programIO[0], 1, strlen(programIO[0]), inFile);
    fwrite(programIO[1], 1, strlen(programIO[1]), outFile);

    // Close the files
    fclose(inFile);
    fclose(outFile);
}