#!/usr/bin/env python
"""
sched.api.py: Library handling resident scheduler model
"""

__author__ = "Liam Kalir"
__copyright__ = "Copyright 2017, Bit. Nibble. Byte."
__credits__ = ["Liam Kalir"]
__license__ = "GPL 3.0"
__verision__ = "0.0.1"
__maintainter__ = "Liam Kalir"
__email__ = "lk8150@rit.edu"
__status__ = "Prototype"

import imp
from pathlib import Path
from pyomo.environ import *


class ModelSolver(object):
    """
    Model solver class

    Attributes:
        modelFile (str): Path to model file
        paramFile (str): Path to parameter file
    """

    def __init__(self, modelFile, paramFile):
        """
        Args:
            modelFile (str): Path to model file
            paramFile (str): Path to parameter file
        """
        super(ModelSolver, self).__init__()

        # Check if files exists
        model_file = Path(modelFile)
        param_file = Path(paramFile)
        if model_file.is_file() and param_file.is_file():
            f, fname, fdesc = imp.find_module('ojModel')
            if f is not None:
                pack = imp.load_module('ojModel', f, fname, fdesc)
                print(pack.model)


if __name__ == "__main__":
    path1 = 'C:\\Users\\Lamu\\Documents\\GitHub\\resident-scheduler\\src\\ojModel.py'
    path2 = 'C:\\Users\\Lamu\\Documents\\GitHub\\resident-scheduler\\src\\ojData.dat'
    mySolver = ModelSolver(path1, path2)
