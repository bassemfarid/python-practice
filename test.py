import math
import os
import subprocess
import sys
import time
from typing import NoReturn, Any
import numbers

# Abstracts ANSI escape codes to help cleanup code
class Colour:
    GREY    = "\033[90m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    RESET   = "\033[0m"


def is_numeric(value: Any) -> bool:
    """Check if a value is numeric (int or float)
    
    Args:
        value (Any): The value to check

    Returns:
        bool: True if value is numeric, False if not
    """
    return isinstance(value, numbers.Number)


def get_timeout(test_folder: str) -> int:
    """
    Get the timeout value.

    Timeout is read from a file named "timeout.txt" in the test folder.
    If the file does not exist or contains an invalid value, defaults to 1 second.

    Args:
        test_folder (str): The test folder to read from
    
    Returns:
        int: The timeout found in test_folder/timeout.txt if found, else defaults to 1
    """
    timeout_file = os.path.join(test_folder, "timeout.txt")
    if os.path.exists(timeout_file):
        try:
            with open(timeout_file, "r") as f:
                timeout = float(f.read().strip())
                return max(1, min(timeout, 5))  # Clamp between 1 and 5 seconds
        except ValueError:
            pass
    return 1


def get_student_script(problem_id: str) -> str | NoReturn:
    """Get the path to the student's script based on the problem ID.
    
    Args:
        problem_id (str): The problem ID
    
    Returns:
        str | NoReturn: The location of the script if found. If there is an error, the program exits
    """
    if "-" not in problem_id:
        print(f"Invalid problem ID format: {problem_id}")
        print("Expected format: <unit>-<chapter>-<problem>")
        sys.exit(1)
    unit, chapter, _ = problem_id.split("-")
    location = os.path.join(f"Unit-{unit}", f"Chapter-{chapter}", f"{problem_id}.py")
    if not os.path.exists(location):
        print(f"Student script not found: {location}")
        sys.exit(1)
    return location

def print_coloured(message: str, colour: str) -> None:
    """Prings a coloured message. Resets the colour after the message
    
    Args:
        message (str): The message to print
        colour (str): The ANSI escape sequence colour to make the message
    """
    print(f"{colour}{message}{Colour.RESET}")

def run_io_test(test_folder: str, student_script: str) -> None:
    """Run all I/O tests in the test folder. Stops on batch failure.
    
    Args:
        test_folder (str): The path of the test folder
        student_script (str): The path to the student's script
    """
    batches = {}
    for f in sorted(os.listdir(test_folder)):
        if f.endswith(".in"):
            batch_name = f.rsplit("-", 1)[0]
            if batch_name not in batches:
                batches[batch_name] = []
            batches[batch_name].append(f[:-3])

    # Orders the batches so that "sample" comes first to fail fast if needed
    sorted_batches = sorted(
        batches.keys(),
        key=lambda x: (x != "sample", int(x) if x.isdigit() else sys.maxsize),
    )

    timeout = get_timeout(test_folder)

    for batch in sorted_batches:
        print("=" * 40)
        print(f"Running batch {batch} tests...")
        for test_id in sorted(batches[batch]):
            expected_output_file = os.path.join(test_folder, f"{test_id}.out")
            if not os.path.exists(expected_output_file):
                print(f"Missing expected output file: {expected_output_file}")
                continue

            input_file = os.path.join(test_folder, f"{test_id}.in")
            passed, io_info, execution_time_ms = run_single_io_test(
                input_file, expected_output_file, student_script, timeout
            )

            if passed:
                print(f"{test_id}: {Colour.GREEN}PASS {Colour.RESET}({execution_time_ms} ms)")
            else:
                # Provide student with failure message, which includes:
                # execution time, input, expected output, actual output
                print(f"{test_id}: {Colour.RED}FAIL {Colour.RESET}({execution_time_ms} ms)")
                if isinstance(io_info, tuple):
                    print_coloured(f"\nOutput does not match expected output:", Colour.YELLOW)
                    print_coloured(f"\nFor Input", Colour.YELLOW)
                    print(io_info[0])
                    print_coloured(f"\nExpected Output:", Colour.YELLOW)
                    print(io_info[1])
                    print_coloured(f"\nActual Output:", Colour.YELLOW)
                    print(io_info[2])
                # Provide instead with the specific exception that was thrown
                else:
                    print_coloured("\nAn Error Occurred:", Colour.YELLOW)
                    print(io_info)
                print("=" * 40)
                if batch == "sample":
                    print("Sample tests failed. Aborting further testing.")
                    return
                else:
                    print(f"Batch {batch} failed. Skipping remaining tests in this batch.")
                    break


def run_single_io_test(input_file: str,
                       expected_output_file: str,
                       student_script: str,
                       timeout: int) -> tuple[bool, str | tuple[str, str, str], int]:
    """Run a single I/O test and return success status and info.
    
    Args:
        input_file (str): The path to the file that contains input data
        expected_output_file (str): The path to the file that contains the expected output
        student_script (str): The path to the student's script
        timeout (int): The max amount of time the student's script is allowed to take
    
    Returns:
        tuple[bool, str | tuple[str, str, str], int]: A tuple which contains the following:
                                                      (Whether the script passed,
                                                      Either an error message or IO data formatted
                                                                                 (input, expected_output, actual_output),
                                                      The execution time in milliseconds)
    """

    # Pull the input and expected output from the files
    with open(input_file, "r") as f:
        input_data = f.read()
    with open(expected_output_file, "r") as f:
        expected_output = f.read().strip()

    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, student_script],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        end_time = time.time()

        execution_time_ms = round((end_time - start_time) * 1000, 2)
        actual_output = result.stdout.strip() if result.stdout else ""

        # Account for floating point errors
        if is_numeric(actual_output) and is_numeric(expected_output):
            passed = math.isclose(float(actual_output), float(expected_output), rel_tol=1e-9)
        else:
            passed = actual_output == expected_output

        return (passed, (input_data, expected_output, actual_output), execution_time_ms)

    except subprocess.TimeoutExpired:
        return (False, "Time Limit Exceeded!", timeout * 1000)

    except Exception as e:
        return (False, str(e), 0)


def run_unit_test(test_script: str) -> bool:
    """Run a unit test script and return success status.
    
    Args:
        test_script (str): The path to the test script
    
    Returns:
        bool: True if the script passed, False if not
    """
    try:
        subprocess.run(
            [sys.executable, test_script],
            check=True,
            timeout=get_timeout(os.path.dirname(test_script)),
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Unit test script {test_script} failed.")
        return False


def main() -> int | None:
    """Main function
    
    Returns:
        int | None: The exit code of the program, None to exit with code 0
    """
    try:
        if len(sys.argv) != 2:
            print("Usage: python test.py <problem_id>")
            return 1

        problem_id = sys.argv[1]
        student_script = get_student_script(problem_id)  # Will exit if not found
        test_folder = os.path.join("tests", problem_id)
        test_script = os.path.join(test_folder, f"test_{problem_id}.py")

        # Ensure the test folder exists
        if not os.path.exists(test_folder):
            print(f"Test folder not found: {test_folder}")
            return 1

        # If a unit test script exists, run it
        # If unit test fails, abort any further testing
        if os.path.exists(test_script):
            if not run_unit_test(test_script):
                print("Unit tests failed. Aborting further testing.")
                return 1

        # If I/O tests are present, run them
        io_test_files = [f for f in os.listdir(test_folder) if f.endswith(".in")]
        if io_test_files:
            run_io_test(test_folder, student_script)

    except Exception as e:
        print(f"An error occurred: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
