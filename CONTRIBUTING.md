# CONTRIBUTING.md

## Contributing to Python Practice

Thank you for your interest in contributing! This repository is designed to help students practice Python through structured problems with automated I/O testing. Your contributions help improve the quality and variety of problems available to learners.

## How You Can Contribute

You are welcome to contribute in the following ways:

### 📖 Improve Question Clarity
- Edit ##-##-##.md files to fix grammar, improve clarity, or enhance explanations.
- Ensure the problem statement aligns with the expected input/output behavior.

### 🔍 Fix Incorrect I/O Test Cases
- If you find a test case that does not match the expected output, fix it.
- Ensure corrections maintain the intended problem difficulty.

### ✅ Add More Test Cases
- Add edge cases, boundary values, or off-by-one scenarios.
- Name test cases following the existing pattern:
    - ##-##-##.X-YY.in (input file)
    - ##-##-##.X-YY.out (expected output file)
    - X represents test difficulty (1 = easy, 2 = medium, etc.)
    - YY is a sequential number (01, 02, etc.).
    - Example: 01-02-01.2-03.in and 01-02-01.2-03.out.

### ✨ Create New Problems
- Submit a new problem following the existing folder structure (Unit-Chapter).
- Include a ##-##-##.md file with a clear description, input format, output format, and sample cases.
- Add at least 3 test cases (one sample and two additional).
- Ensure your problem is distinct from existing ones.

## Contribution Guidelines

### 1️⃣ Fork the Repository

Click the Fork button on GitHub and clone your fork:

```sh
git clone https://github.com/YOUR-USERNAME/python-practice.git
cd python-practice
```

### 2️⃣ Create a New Branch

Use a meaningful branch name:

```sh
git checkout -b fix-typo-in-01-02-01
```

### 3️⃣ Make Changes & Test Locally
- Modify/add files as needed.
- Run main_test_runner.py to ensure no tests break.

```sh
python main_test_runner.py
```

### 4️⃣ Commit Your Changes

Write a clear commit message:

```sh
git add .
git commit -m "Fixed typo in 01-02-01.md and added edge case"
```

### 5️⃣ Push & Open a Pull Request

```sh
git push origin fix-typo-in-01-02-01
```

- Open a Pull Request (PR) on GitHub.
- Explain your changes briefly.
- A reviewer will provide feedback if needed.

### Style Guide
- Follow PEP 8 for Python code.
- Keep problem descriptions concise and structured.
- Use clear variable names and avoid unnecessary complexity.

## Need Help?

If you have any questions, feel free to open an issue or ask in discussions. Happy coding! 🚀
