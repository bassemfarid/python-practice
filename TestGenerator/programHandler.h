#ifndef PROGRAMHANDLER_H
#define PROGRAMHANDLER_H

/**
 * \brief Gets the program name based on the program number
 * \param programNumber The program number formatted "<Unit>-<Chapter>-<Program>"
 * \return The path to the generator program to run
 */
char* programHandler_GetProgramName(char* programNumber);

/**
 * \brief Runs the generator program from \c programHandler_getProgramName and returns its IO
 * \param path The path to the test case generator python program
 * \return The generator's IO
 */
char** programHandler_RunPythonProgram(char* path);

#endif