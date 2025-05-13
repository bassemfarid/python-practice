import importlib.util
import os
import unittest

# Determine problem ID from the script's filename
script_name = os.path.basename(__file__)  # e.g., "test_01-01-01.py"
problem_id = script_name[5:-3]  # Extract "01-01-01" from "test_01-01-01.py"

# Construct the path to the student's solution
unit, chapter, _ = problem_id.split("-")
solution_path = os.path.join(f"Unit-{unit}", f"Chapter-{chapter}", f"{problem_id}.py")

# Dynamically import student solution
spec = importlib.util.spec_from_file_location("student_solution", solution_path)
student_solution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student_solution)


class TestStudentSolution(unittest.TestCase):
    def test_file_read_write(self):
        student_solution.writeToFile("__greet.txt", "Hello!\n")
        student_solution.appendToFile("__greet.txt", "Goodbye!\n")
        # Handled differently to account for file deletion
        if (contents := student_solution.readFromFile("__greet.txt")) != "Hello!\nGoodbye!\n":
            os.remove("__greet.txt")

            # Make contents readable
            contents.replace('\n', "\\n")
            raise AssertionError(f"Contents of the file (should be \"Hello!\\nGoodbye!\\n\"): \"{contents}\"")
        os.remove("__greet.txt")


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=1)
    unittest.main(testRunner=runner)
