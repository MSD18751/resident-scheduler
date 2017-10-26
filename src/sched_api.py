#!/usr/bin/env python
"""
sched.api.py: Library handling resident scheduler model
"""

import importlib
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
        model (PyomoModel.AbstractModel): Pyomo Model
    """

    def __init__(self, modelFile):
        """
        Args:
            modelFile (str): Path to model file
        """
        super(ModelSolver, self).__init__()

        # Check if files exists
        model_file = Path(modelFile)
        if model_file.is_file():
            ldr = importlib.find_loader('ojModel')
            if ldr is not None:
                try:
                    m = ldr.load_module()
                    self.model = m.model
                    self.optimizer = SolverFactory('glpk')
                    self.solved = False
                except ImportError as err:
                    raise err
            else:
                raise IOError
        else:
            raise OSError

    def LoadData(self, dataFile):
        data_file = Path(dataFile)
        if data_file.is_file():
            self.data = DataPortal()
            self.data.load(filename=dataFile, model=self.model)
        else:
            raise OSError

    def Solve(self):
        if not self.solved:
            self.instance = self.model.create_instance(self.data)
            self.optimizer.solve(self.instance)


if __name__ == "__main__":
    path1 = 'ojModel.py'
    path2 = 'ojData.dat'
    mySolver = ModelSolver(path1)
    mySolver.LoadData(path2)
    mySolver.Solve()
    resdict = mySolver.instance.X.get_values()
