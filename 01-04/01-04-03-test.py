import os
import sys

# Get the absolute path to the main repository folder
# (parent of the current folder)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the repo root to sys.path so Python can find main_test_runner.py
sys.path.insert(0, REPO_ROOT)

try:
    from main_test_runner import run_all_tests
except ModuleNotFoundError:
    print(
        "❌ Error: Could not import 'main_test_runner'. Make sure it's in the repository root."
    )
    exit(1)

if __name__ == "__main__":
    # Get current student's script's name (without "-test.py")
    test_script_name = os.path.basename(__file__)
    student_script_name = os.path.join(
        os.path.dirname(__file__), test_script_name.replace("-test", "")
    )

    # Find the test folder (ends in -tests)
    test_folder = os.path.join(
        os.path.dirname(__file__), student_script_name.replace(".py", "-tests")
    )

    if not os.path.exists(student_script_name):
        print(f"❌ Student script '{student_script_name}' not found.")
        exit(1)

    if not os.path.exists(test_folder):
        print(f"❌ Test folder '{test_folder}' not found.")
        exit(1)

    run_all_tests(student_script_name, test_folder)
