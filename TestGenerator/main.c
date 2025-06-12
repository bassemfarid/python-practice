#include <stdio.h>
#include <stdlib.h>
#include "programHandler.h"
#include "caseHandler.h"
#include "constants.h"

#include <string.h>
int main(int argc, char** argv) {
    if(argc != 2) {
        printf("Usage: %s <Program Number>\n", argv[0]);
        return 1;
    }

    // Get the base path
    constants_GetBasePath();

    // Run the program and get the input/output
    char* name = programHandler_GetProgramName(argv[1]);
    char** programIO = programHandler_RunPythonProgram(name);
    free(name);

    // Write the test case
    int nextCase = caseHandler_GetNextCase(argv[1]);
    caseHandler_PopulateNextCase(argv[1], nextCase, programIO);

    free(programIO[0]);
    free(programIO[1]);
    free(programIO);

    printf("Wrote test %d!\n", nextCase);
}
