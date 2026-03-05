# Python Practice

## How to Solve Problems

1. **Fork and Clone** – Fork this repository and clone it to your local machine.
2. **Read the Problem** – Open the `XX-XX-XX.md` file in the problem folder to review the instructions.
3. **Write Your Code** – Create a `XX-XX-XX.py` file in the same folder and implement your solution.
4. **Test Your Solution** – Run the following command in the terminal:

   ```sh
    # On macOS/Linux
    python3 test.py XX-XX-XX

    # On Windows
    python test.py XX-XX-XX
   ```

**NOTE:** Replace `XX-XX-XX` with the problem ID (e.g., `01-02-01`). The ID format is `Unit-Chapter-Question`, so `01-02-01` corresponds to the file at `Unit-01/Chapter-02/01-02-01.py`. This will automatically check your solution using the provided test cases.

You can also run all tests at once to check your overall progress:

```sh
# On macOS/Linux
python3 test.py

# On Windows
python test.py
```

### Understanding Test Output

- **Sample tests** run first. If a sample test fails, all further testing for that problem is aborted — fix the sample case before moving on.
- **Batch tests** (1, 2, 3, ...) run in order of difficulty. If a test fails within a batch, the remaining tests in that batch are skipped, but later batches still run.
- The output shows how many tests were skipped so you know what wasn't checked.

## Keeping Your Repository Updated

When new problems are added, you'll need to pull updates from the original repository into your copy.


1. **Add Upstream Remote** – Run this once inside your local repository (skip this step if you already added it):

    ```sh
    git remote add upstream https://github.com/bassemfarid/python-practice.git
    ```

2. **Pull the Latest Updates** – Fetch the updates and merge them:

    ```sh
    git pull upstream main
    ```
    If Git reports conflicts, open the files it lists, keep the code you want, delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), save the file, then commit:
    ```sh
    git add .
    git commit -m "Resolved merge conflicts"
    ```

## File Structure
```
python-practice/
│── test.py  # Central test script
│── README.md
│── .gitignore
│
├── Unit-01/  # Unit folder
│   ├── Chapter-02/  # Chapter folder
│   │   ├── 01-02-01.py  # Student creates this script
│   │   ├── 01-02-01.md  # Problem details
│   │   ├── ...
│
├── tests/
│   ├── 01-02-01/  # Problem-specific test folder
│   │   ├── test_01-02-01.py  # Unit test script (if needed)
│   │   ├── timeout.txt  # Optional timeout override (if present)
│   │   ├── sample-01.in  # Sample I/O test input
│   │   ├── sample-01.out  # Sample I/O test output
│   │   ├── 1-01.in  # Batch 1, test case 1 input
│   │   ├── 1-01.out  # Batch 1, test case 1 output
│   │   ├── 1-02.in  # Batch 1, test case 2 input
│   │   ├── 1-02.out  # Batch 1, test case 2 output
│   │   ├── 2-01.in  # Batch 2, test case 1 input
│   │   ├── 2-01.out  # Batch 2, test case 1 output
│   │   ├── ...
│   │
│   ├── 01-02-02/  # Another problem's test folder
│   │   ├── sample-01.in
│   │   ├── sample-01.out
│   │   ├── 1-01.in
│   │   ├── 1-01.out
│   │   ├── ...
```
