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

**NOTE:** Replace XX-XX-XX with the problem ID (e.g., 01-02-01). This will automatically check your solution using the provided test cases.

## Keeping Your Repository Updated

When new problems are added, you’ll need to pull updates from the original repository into your copy.


1. **Add Upstream Remote** – Run this once inside your local repository (replace if you already added it):

    ```sh
    git remote add upstream https://github.com/bassemfarid/python-practice.git
    ```

2. **Pull the Latest Updates** – Fetch the updates and merge them:

    ```sh
    git pull upstream main
    ```
    If Git reports conflicts, open the files it lists, fix the <<<<<<< >>>>>>> sections, then commit.

3. **Commit (if needed)** – If the pull created changes, finish with:
    ```sh
    git commit -m "Merged updates from upstream"
    ```
    This way, you’ll get the new problems and tests without losing your own work.

## File Structure
```
python-practice/
│── test.py  # Central test script
│── README.md
│── main.py  # Code playground without tests
│── .gitignore
│── .venv/
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