# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational Python practice repository where students solve programming problems organized by Unit and Chapter. Each problem has a markdown description (`XX-XX-XX.md`) and students create corresponding solution files (`XX-XX-XX.py`) in the same folder. The ID format is `UU-CC-QQ` (Unit-Chapter-Question).

## Testing

**Run tests for a specific problem:**
```sh
python3 test.py XX-XX-XX
```

**Run all tests (checks every problem that has both a solution file and test folder):**
```sh
python3 test.py
```

The test runner (`test.py`) supports two types of tests per problem:
- **I/O tests**: Input/output file pairs in `tests/XX-XX-XX/` (e.g., `sample-01.in`/`sample-01.out`, `1-01.in`/`1-01.out`). Sample tests run first and abort all testing on failure. Batch tests skip remaining cases in a batch on failure but continue to other batches.
- **Unit tests**: Optional `test_XX-XX-XX.py` scripts in the test folder that use `unittest` and dynamically import the student's solution module.

Floating-point outputs are compared token-by-token per line using `math.isclose(rel_tol=1e-9)`, so multiline and mixed text/numeric outputs are handled correctly. Default timeout is 1 second per I/O test case, overridable via `timeout.txt` in the test folder (clamped 1-5 seconds). Unit test scripts use 5x the timeout value to accommodate multiple test methods.

## Repository Structure

```
Unit-XX/Chapter-YY/         # Problem descriptions (.md) and student solutions (.py)
tests/XX-XX-XX/             # Test data per problem: .in/.out pairs, optional test_*.py and timeout.txt
test.py                     # Central test runner
```

## Problem File Conventions

- Problem descriptions use LaTeX math notation (`$variable$`, `$$formula$$`) and code blocks for sample I/O
- Solutions are standalone Python scripts that read from stdin and print to stdout (for I/O-tested problems)
- For unit-tested problems (e.g., Unit 2 Chapters 1-2, Unit 5+), solutions define functions that are imported by the test script. Some unit tests enforce constraints (e.g., no `if` statements allowed).

## Contributing Problems

Test case naming: `X-YY.in`/`X-YY.out` where X = difficulty batch (1=easy, 2=medium, etc.), YY = sequential number. Sample cases use `sample-XX.in`/`sample-XX.out`. Follow PEP 8 for any Python code.
