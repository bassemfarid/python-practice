# Readme

## How to Solve Problems

1. Open the ##-##-##.md file in each folder to read the problem instructions.
2. Create a ##-##-##.py file in the same folder.
3. Write your program solution according to the problem instructions.
4. Run the ##-##-##-test.py file in the same folder. Adjust your program until all tests pass.

## Getting Updates

As new problems are added, you’ll need to pull updates into your fork.

First, ensure this repository is set as the upstream remote. If it’s not, add it by the following command, where YOUR-ORG is your organization name:

```sh
git remote add upstream https://github.com/YOUR-ORG/python-practice.git
```

Then, fetch updates and merge them:

```sh
git fetch upstream
git merge upstream/main --no-commit --no-ff
```

This won’t overwrite your solutions but will add new problems and tests.

## File Structure
```
python-practice/  
│── main_test_runner.py  # Central test script
│── README.md
│── main.py  # Code playground without tests
│── .gitignore  
│── .venv/
│  
├── 01-02/  # Unit-Chapter
│   │── 01-02-01.py  # Students create this script 
│   │── 01-02-01-test.py  # Runs tests for the problem
│   ├── 01-02-01-tests/  # Test cases  
│   │   ├── 01-02-01.1-01.in  
│   │   ├── 01-02-01.1-01.out  
│   │   ├── 01-02-01.sample-01.in  
│   │   ├── 01-02-01.sample-01.out  
│  
├── 01-03/  
│   ├── ...  
```