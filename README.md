# Python Practice

## How to Solve Problems

1. Begin by forking this repository, then cloning it to your local machine.
2. Open the ##-##-##.md file in each folder to read the problem instructions.
3. Create a ##-##-##.py file in the same folder. You must do this for each problem.
4. Write your program solution according to the problem instructions.
5. Run the ##-##-##-test.py file in the same folder. Adjust your program until all tests pass.

## Getting Updates

As new problems are added, you’ll need to pull updates into your fork.

First, ensure this repository is set as the upstream remote. If it’s not, add it:

```sh
git remote add upstream https://github.com/bassemfarid/python-practice.git
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
│   │── 01-02-01.py  # Student created script
│   │── 01-02-01-test.py  # Runs tests for the problem
│   ├── 01-02-01-tests/  # Test cases folder
│   │   ├── 01-02-01.1-01.in
│   │   ├── 01-02-01.1-01.out
│   │   ├── 01-02-01.sample-01.in
│   │   ├── 01-02-01.sample-01.out
│
├── 01-03/
│   ├── 01-03.md  # instructions for activity
|
├── 01-04/
|   ├── 01-04-0X.py  # Student created script
|   ├── 01-04-0X-test.py  # Runs tests for the problem
|   ├── 01-04-01-tests/  # Test cases folder
│   │   ├── 01-04-0X.1-0X.in
│   │   ├── 01-04-0X.1-0X.out
│   │   ├── 01-04-0X.sample-01.in
│   │   ├── 01-04-0X.sample-01.out
|
├── 01-05/
|   ├── 01-05-0X.py  # Student created script
|   ├── 01-05-0X-test.py  # Runs tests for the problem
│   ├── 01-05-0X-tests/  # Test cases folder
│   │   ├── 01-05-01.sample-01.in
│   │   ├── 01-05-01.sample-01.out

```