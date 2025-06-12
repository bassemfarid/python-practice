#ifndef CASEHANDLER_H
#define CASEHANDLER_H

/**
 * \brief Gets the next case yet to be populated. For example, if 1-01.in and 1-02.in
 *        existed, this function would return 3 because 1-03.in is the next case to fill
 * \param programNumber The program number formatted as "<Unit>-<Chapter>-<Program>"
 * \return The next case yet to be filled
 */
int caseHandler_GetNextCase(char* programNumber);

/**
 * \brief Populates a case's .in and .out files
 * \param programNumber The program number formatted as "<Unit>-<Chapter>-<Program>"
 * \param caseNumber The case number to populate
 * \param programIO The IO gathered from the generator program
 */
void caseHandler_PopulateNextCase(char* programNumber, int caseNumber, char** programIO);

#endif