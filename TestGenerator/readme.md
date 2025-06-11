# Test Generator

## Usage

Just create a generator.py file in the test folder you want to write tests for
Run the program with the test ID and let it handle everything for you \
For example, to generate tests for program 01-06-01, run "[./]TestGenerator 01-06-01"
and follow the steps from there

## Modifying

The source code for the TestGenerator is all within this directory. Just be sure
to modify **C_CODE_PATH** in [constants.h](constants.h) if you are on Windows or errors won't print properly

I've compiled using GCC on both windows and linux, but everything used here should be standard