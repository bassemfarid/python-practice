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
    def test_ordinal_suffix(self):
        self.assertEqual(student_solution.ordinalSuffix(0), "0th")
        self.assertEqual(student_solution.ordinalSuffix(1), "1st")
        self.assertEqual(student_solution.ordinalSuffix(2), "2nd")
        self.assertEqual(student_solution.ordinalSuffix(3), "3rd")
        self.assertEqual(student_solution.ordinalSuffix(4), "4th")
        self.assertEqual(student_solution.ordinalSuffix(10), "10th")
        self.assertEqual(student_solution.ordinalSuffix(11), "11th")
        self.assertEqual(student_solution.ordinalSuffix(12), "12th")
        self.assertEqual(student_solution.ordinalSuffix(13), "13th")
        self.assertEqual(student_solution.ordinalSuffix(14), "14th")
        self.assertEqual(student_solution.ordinalSuffix(101), "101st")


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
