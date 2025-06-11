#ifndef ERROR_H
#define ERROR_H

#include <stdarg.h>

_Noreturn void __error(int lineNumber, const char* fileName, const char* format, ...);

/**
 * \brief Prints out an error message and exits the program. error(NULL) to exit normally.
 *        Takes in arguments just like printf and prints them to stderr before exiting
 */
#define error(___format, ...) __error(__LINE__, __FILE__, ___format, ##__VA_ARGS__)

#endif