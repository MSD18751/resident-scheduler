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
            ModelSolver("dummyModel.py")
            _pass = True
        except Exception as err:
            pass

        self.assertTrue(_pass)

        # No file
        with self.assertRaises(OSError):
            ModelSolver("FAKEFILE")

        # File found, but it can't be imported
        with self.assertRaises(ImportError):
            ModelSolver("not_a_python_file.txt")

        # Python file found, but not a Pyomo model
        with self.assertRaises(AttributeError):
            ModelSolver("test.py")

        # Check if param is a string
        with self.assertRaises(TypeError):
            ModelSolver(5)

    def test_data_load(self):
        """
        Tests model data loading method
        """

        _ms = ModelSolver("dummyModel.py")

        # No data file
        _ms.load_data(None, load_data=False)
        self.assertEqual(True, _ms._data is None)
        self.assertEqual(True, _ms._instance is not None)

        _ms = ModelSolver("ojModel.py")
        _ms.load_data("ojData.dat")
        self.assertEqual(True, _ms._data is not None)
        self.asssertEqual(True, _ms._instance is not None)


# Run tests
if __name__ == "__main__":
    unittest.main()
