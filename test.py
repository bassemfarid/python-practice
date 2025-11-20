import math
import os
import subprocess
import sys
import time


# Abstracts ANSI escape codes to help cleanup code
class Colour:
    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"


def is_numeric(value):
    """Check if a value is numeric (int or float)."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def get_timeout(test_folder):
    """
    Get the timeout value.

    Timeout is read from a file named "timeout.txt" in the test folder.
    If the file does not exist or contains an invalid value, defaults to 1 second.
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


def get_student_script(problem_id):
    """Get the path to the student's script based on the problem ID."""
    if "-" not in problem_id:
        print(f"Invalid problem ID format: {problem_id}")
        print("Expected format: <unit>-<chapter>-<problem>")
        raise ValueError("Invalid problem ID format")
    unit, chapter, _ = problem_id.split("-")
    location = os.path.join(f"Unit-{unit}", f"Chapter-{chapter}", f"{problem_id}.py")
    if not os.path.exists(location):
        # print(f"Student script not found: {location}") # Let caller handle printing if needed
        raise FileNotFoundError(f"Student script not found: {location}")
    return location


def print_coloured(message, colour):
    """Prings a coloured message. Resets the colour after the message."""
    print(f"{colour}{message}{Colour.RESET}")


def run_io_test(test_folder, student_script):
    """Run all I/O tests in the test folder. Stops on batch failure."""
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

    passed_count = 0
    failed_count = 0

    for batch in sorted_batches:
        print("=" * 40)
        print(f"Running batch {batch} tests...")
        batch_failed = False
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
                passed_count += 1
            else:
                # Provide student with failure message
                print(f"{test_id}: {Colour.RED}FAIL {Colour.RESET}({execution_time_ms} ms)")
                if isinstance(io_info, tuple):
                    print_coloured("\nOutput does not match expected output:", Colour.YELLOW)
                    print_coloured("\nFor Input", Colour.YELLOW)
                    print(io_info[0])
                    print_coloured("\nExpected Output:", Colour.YELLOW)
                    print(io_info[1])
                    print_coloured("\nActual Output:", Colour.YELLOW)
                    print(io_info[2])
                else:
                    print_coloured("\nAn Error Occurred:", Colour.YELLOW)
                    print(io_info)
                print("=" * 40)
                failed_count += 1
                batch_failed = True
                
                if batch == "sample":
                    print("Sample tests failed. Aborting further testing.")
                    return (passed_count, failed_count)
                else:
                    print(f"Batch {batch} failed. Skipping remaining tests in this batch.")
                    break
        
        if batch_failed:
             # If a batch failed, we might skip subsequent batches? 
             # The original code didn't explicitly break the outer loop on non-sample failure,
             # but `run_io_test` logic was a bit loose.
             # Actually, looking at original code:
             # if batch == "sample": return
             # else: break (breaks inner loop) -> continues to next batch?
             # Wait, `break` breaks the inner loop (tests in batch).
             # Then it goes to next batch.
             # So it continues testing other batches?
             # "Skipping remaining tests in this batch." implies yes.
             pass

    return (passed_count, failed_count)


def run_single_io_test(input_file, expected_output_file, student_script, timeout):
    """Run a single I/O test and return success status and info."""

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


def run_unit_test(test_script):
    """Run a unit test script and return (passed_count, failed_count)."""
    try:
        subprocess.run(
            [sys.executable, test_script],
            check=True,
            timeout=get_timeout(os.path.dirname(test_script)),
        )
        return (1, 0)
    except subprocess.CalledProcessError:
        print(f"Unit test script {test_script} failed.")
        return (0, 1)


def run_tests_for_problem(problem_id):
    """Run tests for a specific problem ID. Returns ('PASS'/'FAIL'/'SKIP', passed_count, failed_count)."""
    try:
        try:
            student_script = get_student_script(problem_id)
        except FileNotFoundError as e:
            print(f"Skipping {problem_id}: {e}")
            return ("SKIP", 0, 0)
        except ValueError as e:
            print(f"Skipping {problem_id}: {e}")
            return ("SKIP", 0, 0)

        test_folder = os.path.join("tests", problem_id)
        test_script = os.path.join(test_folder, f"test_{problem_id}.py")

        # Ensure the test folder exists
        if not os.path.exists(test_folder):
            print(f"Test folder not found: {test_folder}")
            return ("SKIP", 0, 0)

        print(f"\nRunning tests for {problem_id}...")

        total_passed = 0
        total_failed = 0
        problem_failed = False

        # If a unit test script exists, run it
        if os.path.exists(test_script):
            u_pass, u_fail = run_unit_test(test_script)
            total_passed += u_pass
            total_failed += u_fail
            if u_fail > 0:
                print(f"Unit tests failed for {problem_id}.")
                problem_failed = True

        # If I/O tests are present, run them
        io_test_files = [f for f in os.listdir(test_folder) if f.endswith(".in")]
        if io_test_files:
            io_pass, io_fail = run_io_test(test_folder, student_script)
            total_passed += io_pass
            total_failed += io_fail
            if io_fail > 0:
                problem_failed = True
        
        if problem_failed:
            return ("FAIL", total_passed, total_failed)
        else:
            return ("PASS", total_passed, total_failed)

    except Exception as e:
        print(f"An error occurred while testing {problem_id}: {e}")
        return ("FAIL", 0, 0)


def main():
    # If arguments are provided, run for specific problem
    if len(sys.argv) > 1:
        problem_id = sys.argv[1]
        run_tests_for_problem(problem_id)
        return 0

    # Otherwise, run all tests
    print("Running all tests...")
    tests_dir = "tests"
    if not os.path.exists(tests_dir):
        print("Tests directory not found.")
        return 1

    # Get all subdirectories in tests/
    problem_ids = [d for d in os.listdir(tests_dir) if os.path.isdir(os.path.join(tests_dir, d))]
    
    def sort_key(pid):
        parts = pid.split('-')
        return [int(p) if p.isdigit() else p for p in parts]
    
    problem_ids.sort(key=sort_key)

    question_stats = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    test_case_stats = {"PASS": 0, "FAIL": 0}
    total_questions = 0

    for problem_id in problem_ids:
        total_questions += 1
        status, p_count, f_count = run_tests_for_problem(problem_id)
        question_stats[status] += 1
        test_case_stats["PASS"] += p_count
        test_case_stats["FAIL"] += f_count
        print("-" * 50)

    print("\n" + "=" * 40)
    print("           TEST SUMMARY")
    print("=" * 40)
    print(f"QUESTIONS CHECKED:      {total_questions}")
    print(f"Questions Fully Passed: {Colour.GREEN}{question_stats['PASS']}{Colour.RESET}")
    print(f"Questions Failed:       {Colour.RED}{question_stats['FAIL']}{Colour.RESET}")
    print(f"Questions Skipped:      {Colour.YELLOW}{question_stats['SKIP']}{Colour.RESET}")
    print("-" * 40)
    print(f"Total Test Cases Passed: {Colour.GREEN}{test_case_stats['PASS']}{Colour.RESET}")
    print(f"Total Test Cases Failed: {Colour.RED}{test_case_stats['FAIL']}{Colour.RESET}")
    print("=" * 40)

    return 0 if question_stats["FAIL"] == 0 else 1


if __name__ == "__main__":
    exit(main())
