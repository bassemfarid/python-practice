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
    def test_convert_to_celsius(self):
        self.assertAlmostEqual(student_solution.convertToCelsius(0), -17.77777777777778)
        self.assertAlmostEqual(student_solution.convertToCelsius(180), 82.22222222222223)

    def test_convert_to_fahrenheit(self):
        self.assertAlmostEqual(student_solution.convertToFahrenheit(0), 32)
        self.assertAlmostEqual(student_solution.convertToFahrenheit(100), 212)

    def test_inverse(self):
        val = 15
        f = student_solution.convertToFahrenheit(val)
        c = student_solution.convertToCelsius(f)
        self.assertAlmostEqual(c, val)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=0)
    unittest.main(testRunner=runner)
