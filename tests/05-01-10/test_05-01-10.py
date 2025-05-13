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
    def test_get_hours_minutes_seconds(self):
        self.assertEqual(student_solution.getHoursMinutesSeconds(30), "30s")
        self.assertEqual(student_solution.getHoursMinutesSeconds(60), "1m")
        self.assertEqual(student_solution.getHoursMinutesSeconds(90), "1m 30s")
        self.assertEqual(student_solution.getHoursMinutesSeconds(3600), "1h")
        self.assertEqual(student_solution.getHoursMinutesSeconds(3601), "1h 1s")
        self.assertEqual(student_solution.getHoursMinutesSeconds(3661), "1h 1m 1s")
        self.assertTrue(student_solution.getHoursMinutesSeconds(90042) in ["25h 42s", "1d 1h 42s"])
        self.assertEqual(student_solution.getHoursMinutesSeconds(0), "0s")


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
