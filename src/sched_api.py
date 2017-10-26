#!/usr/bin/env python
"""
sched.api.py: Library handling resident scheduler model
"""

import importlib
import os

from pathlib import Path
from pyomo.environ import *

__author__ = "Liam Kalir"
__copyright__ = "Copyright 2017, Bit. Nibble. Byte."
__credits__ = ["Liam Kalir"]
__license__ = "GPL 3.0"
__verision__ = "0.0.1"
__maintainter__ = "Liam Kalir"
__email__ = "lk8150@rit.edu"
__status__ = "Prototype"


class ModelSolver(object):
    """
    Model solver class

    Attributes:
        _data: Pyomo data portal object
        _instance: Pyomo solver instance object
        _model: Pyomo model object
        _optimizer: Pyomo optimizer object
        _solved: Flag indicating whether a solution has been generated or not
    """

    def __init__(self, model_file):
        """
        Instantiates a ModelSolver object. Loads a Pyomo model from the given
        file and creates a glpk optimizer object as well.

        Args:
            model_file (str): Path to model file

        Raises:
            ImportError: Module cannot be loaded
            AttributeError: Module does not have a 'model'
            IOError: Module does not have a loader
            OSError: File does not exists
        """
        super(ModelSolver, self).__init__()

        # Inialize fields
        self._data = None
        self._instance = None
        self._model = None
        self._optimizer = None
        self._solved = False
        self._vars = None

        # Check if files exists
        _model_file = Path(model_file)
        if _model_file.is_file():
            _ldr = importlib.find_loader(os.path.splitext(model_file)[0])
            # Module exists, load it
            if _ldr is not None:
                try:
                    _modelModule = _ldr.load_module()
                    self._model = _modelModule.model
                    self._optimizer = SolverFactory("glpk")
                except ImportError as err:
                    raise err
                except AttributeError as err:
                    raise err
            else:
                raise IOError("Could not load module")
        else:
            raise OSError("Model file not found")

    def load_data(self, data_file, load_data=True):
        """
        Loads the data from the given data file

        Args:
            data_file (str): Path to data file to load
            load_data (bool): If model requires external data

        Raises:
            OSError: Data file does not exists
        """
        if load_data:
            _data_file = Path(data_file)
            if _data_file.is_file():
                self._data = DataPortal()
                self._data.load(filename=data_file, model=self._model)
            else:
                raise OSError("Data file not found")

        self._instance = self._model.create_instance(self._data)

    def solve(self):
        """
        Attempts to solve the given model

        Raises:
            AttributeError: If model is not properly initialzed for solving
        """
        if all([not self._solved, self._optimizer, self._instance]):
            self._optimizer.solve(self._instance)
        else:
            raise AttributeError("Model not ready for solving")

        self._vars = {}
        for _objs in self._instance.component_objects(Var, active=True):
            _v_objs = getattr(self._instance, str(_objs))
            for index in _v_objs:
                self._vars[index] = _v_objs[index].value


if __name__ == "__main__":
    path1 = "ojModel.py"
    path2 = "ojData.dat"
    try:
        mySolver = ModelSolver(path1)
        mySolver.load_data(path2)
        mySolver.solve()
        print(mySolver._vars)
    except IOError as err:
        raise err
    except OSError as err:
        raise err
