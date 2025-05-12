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
    def test_find_and_replace(self):
        self.assertEqual(student_solution.findAndReplace("The fox", "fox", "dog"), "The dog")
        self.assertEqual(student_solution.findAndReplace("fox", "fox", "dog"), "dog")
        self.assertEqual(student_solution.findAndReplace("Firefox", "fox", "dog"), "Firedog")
        self.assertEqual(student_solution.findAndReplace("foxfox", "fox", "dog"), "dogdog")
        self.assertEqual(student_solution.findAndReplace("The Fox and fox.", "fox", "dog"), "The Fox and dog.")


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=1)
    unittest.main(testRunner=runner)
