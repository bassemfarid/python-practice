import os
import subprocess
import sys
import time

# Configuration
TIMEOUT_SECONDS = 2  # Adjust as needed


def run_test(
    student_script,
    input_file,
    expected_output_file,
    timeout_time=TIMEOUT_SECONDS,
):
    """Runs the student script with input_file and compares it to expected_output_file."""
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
            timeout=timeout_time,  # Prevent infinite loops
        )
        end_time = time.time()

        execution_time_ms = round((end_time - start_time) * 1000, 2)
        actual_output = result.stdout.strip()

        passed = actual_output == expected_output
        return passed, actual_output, execution_time_ms

    except subprocess.TimeoutExpired:
        return False, "Timed out", TIMEOUT_SECONDS * 1000

    except Exception as e:
        return False, str(e), 0


def run_all_tests(student_script, test_folder):
    """Runs all tests in the given folder."""
    test_prefix = os.path.basename(student_script).rsplit(".", 1)[0]
    test_files = sorted(
        f
        for f in os.listdir(test_folder)
        if f.startswith(test_prefix) and f.endswith(".in")
    )

    total_tests = len(test_files)
    passed_tests = 0

    if total_tests == 0:
        print(
            f"⚠️ No test files found in '{test_folder}' for '{student_script}'."
        )
        return

    for test_file in test_files:
        test_num = test_file.split(".")[
            -2
        ]  # Extract test number (e.g., '01' from '01-02-01.01.in')
        expected_output_file = os.path.join(
            test_folder, test_file.replace(".in", ".out")
        )

        if not os.path.exists(expected_output_file):
            print(
                f"Skipping {test_file}: No corresponding {expected_output_file}"
            )
            continue

        input_file_path = os.path.join(test_folder, test_file)
        passed, output, exec_time = run_test(
            student_script, input_file_path, expected_output_file
        )

        if passed:
            print(f"✅ Test {test_num} passed in {exec_time} ms")
            passed_tests += 1
        else:
            print(f"❌ Test {test_num} failed in {exec_time} ms")
            print(f"   Expected: {open(expected_output_file).read().strip()}")
            print(f"   Got: {output}")

    print(f"\n{passed_tests}/{total_tests} tests passed.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python main_test_runner.py <student_script> <test_folder>"
        )
        exit(1)

    student_script = sys.argv[1]
    test_folder = sys.argv[2]

    run_all_tests(student_script, test_folder)
