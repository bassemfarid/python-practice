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
    def test_area(self):
        self.assertEqual(student_solution.area(10, 10), 100)
        self.assertEqual(student_solution.area(0, 9999), 0)
        self.assertEqual(student_solution.area(5, 8), 40)

    def test_perimeter(self):
        self.assertEqual(student_solution.perimeter(10, 10), 40)
        self.assertEqual(student_solution.perimeter(0, 9999), 19998)
        self.assertEqual(student_solution.perimeter(5, 8), 26)

    def test_volume(self):
        self.assertEqual(student_solution.volume(10, 10, 10), 1000)
        self.assertEqual(student_solution.volume(9999, 0, 9999), 0)
        self.assertEqual(student_solution.volume(5, 8, 10), 400)
    
    def test_surface_area(self):
        self.assertEqual(student_solution.surfaceArea(10, 10, 10), 600)
        self.assertEqual(student_solution.surfaceArea(9999, 0, 9999), 199960002)
        self.assertEqual(student_solution.surfaceArea(5, 8, 10), 0)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=1)
    unittest.main(testRunner=runner)
