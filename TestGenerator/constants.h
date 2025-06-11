#ifndef CONSTANTS_H
#define CONSTANTS_H

#define MAX_PROGRAM_PATH_SIZE 2048

#define INPUT_BUFFER_SIZE 4096

#define PROGRAMIO_INITIAL_SIZE 4096
#define PROGRAMIO_STEP_SIZE    4096

// In milliseconds
#define OUTPUT_DELAY 100

// Fill this in yourself. Only necessary on Windows
#define C_CODE_PATH ""

// Populated at the beginning of runtime
extern char BASE_PATH[];
void constants_GetBasePath(void);

#endif
