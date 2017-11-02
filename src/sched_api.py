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

        if not isinstance(model_file, str):
            raise TypeError("Path must be a string")

        # Check if files exists
        _model_file = Path(model_file)
        if _model_file.is_file():
            try:
                _modelModule = importlib.import_module(
                    os.path.splitext(model_file)[0])
                self._model = _modelModule.model
                self._optimizer = SolverFactory("glpk")
            except ImportError as err:
                raise err
            except AttributeError as err:
                raise err
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

        # Extract variables
        self._vars = {}
        for _var in self._instance.component_objects(Var, active=True):
            _v_var = getattr(self._instance, str(_var))
            self._vars[_v_var.name] = {}
            for index in _v_var:
                self._vars[_v_var.name][index] = _v_var[index].value

        # Extract parameters
        self._params = {}
        for _param in self._instance.component_objects(Param, active=True):
            _v_param = getattr(self._instance, str(_param))
            self._params[str(_v_param)] = _v_param._data

        # Extract sets
        self._sets = {}
        for _set in self._instance.component_objects(Set, active=True):
            _v_set = getattr(self._instance, str(_set))
            if _v_set._implicit_subsets is None:
                self._sets[_v_set.name] = _v_set.value

        # Extract objectives
        self._objectives = {}
        for _obj in self._instance.component_objects(Objective, active=True):
            _v_obj = getattr(self._instance, str(_obj))
            self._objectives[_v_obj.name] = _v_obj.expr()

        # Extract constraints
        self._constraints = {}
        for _con in self._instance.component_objects(Constraint, active=True):
            _v_con = getattr(self._instance, str(_con))
            self._constraints[_v_con.name] = {}
            for index in _v_con:
                # Probably not the best way to do this, but it works!
                self._constraints[_v_con.name]['lower'] = \
                    _v_con[index].lower.__str__()
                self._constraints[_v_con.name]['upper'] = \
                    _v_con[index].upper.__str__()
                self._constraints[_v_con.name]['body'] = \
                    _v_con[index].body.__call__()


if __name__ == "__main__":
    path1 = "ojModel.py"
    path2 = "ojData.dat"
    try:
        mySolver = ModelSolver(path1)
        mySolver.load_data(path2)
        mySolver.solve()
        print(mySolver._vars)
        print(mySolver._params)
        print(mySolver._sets)
        print(mySolver._objectives)
        print(mySolver._constraints)
    except IOError as err:
        raise err
    except OSError as err:
        raise err
    except TypeError as err:
        raise err
