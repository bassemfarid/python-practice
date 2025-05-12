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
    def test_square_colours(self):
        # Get the student func and be sure to account for spelling errors
        if hasattr(student_solution, "getChessSquareColour"):
            student_func = student_solution.getChessSquareColour
        elif hasattr(student_solution, "getChessSquareColor"):
            student_func = student_solution.getChessSquareColor
        else:
            raise NameError("No getChessSquareColour or getChessSquareColor found in solution")
        
        # Perform the tests
        self.assertEqual(student_func(1, 1), "white")
        self.assertEqual(student_func(2, 1), "black")
        self.assertEqual(student_func(1, 2), "black")
        self.assertEqual(student_func(8, 8), "white")
        self.assertEqual(student_func(0, 8), "")
        self.assertEqual(student_func(2, 9), "")


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=1)
    unittest.main(testRunner=runner)
