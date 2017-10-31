import unittest

from __init__ import *
from sched_api import ModelSolver


class TestAPI(unittest.TestCase):

    def test_init(self):
        """
        Tests that ModelSolver constructor appropriately handles all cases
        """

        # Good import
        _pass = False
        try:
            _ms = ModelSolver("dummyModel.py")
            _pass = True
        except Exception as err:
            pass

        self.assertTrue(_pass)

        # No file
        with self.assertRaises(OSError):
            _ms = ModelSolver("FAKEFILE")

        # File found, but it can't be imported
        with self.assertRaises(ImportError):
            _ms = ModelSolver("not_a_python_file.txt")

        # Python file found, but not a Pyomo model
        with self.assertRaises(AttributeError):
            _ms = ModelSolver("test.py")

        # Check if param is a string
        with self.assertRaises(TypeError):
            _ms = ModelSolver(5)

    def test_data_load(self):
        """
        Tests model data loading method
        """

        _ms = ModelSolver("dummyModel.py")

        # fug
        _pass = False


# Run tests
if __name__ == "__main__":
    unittest.main()
