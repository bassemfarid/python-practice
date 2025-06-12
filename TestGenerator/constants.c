#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef WIN32
#include <windows.h>
#define PATH_SEPARATOR '\\'
#else
#include <unistd.h>
#include <limits.h>
#define PATH_SEPARATOR '/'
#endif
#include "error.h"
#include "constants.h"

char BASE_PATH[MAX_PROGRAM_PATH_SIZE];

void constants_GetBasePath(void) {
    char exePath[MAX_PROGRAM_PATH_SIZE];

    #ifdef WIN32
    DWORD length = GetModuleFileNameA(NULL, exePath, MAX_PROGRAM_PATH_SIZE);
    if(!length || length == MAX_PROGRAM_PATH_SIZE)
        error("Failed to get the executable's path\n");
    #else
    int length = readlink("/proc/self/exe", exePath, MAX_PROGRAM_PATH_SIZE-1);
    if(length == -1)
        error("Readlink failed\n");
    exePath[length] = 0;
    #endif

    // Remove the executable's name and go up one directory
    char* lastSep = strrchr(exePath, PATH_SEPARATOR);
    if(lastSep) *lastSep = 0;
    lastSep = strrchr(exePath, PATH_SEPARATOR);
    if(lastSep) *lastSep = 0;

    strncpy(BASE_PATH, exePath, MAX_PROGRAM_PATH_SIZE-1);
}