import pandas as pd
import pyomo.environ as pyomo
from pyomo.opt import SolverFactory

def read_excel(filename):
    """Read special Excel spreadsheet to input dict.
    
    Args:
        filename: path to a spreadsheet file
        
    Returns
        dict of DataFrames, to be passed to create_model()
    """
    with pd.ExcelFile(filename) as xls:
        units = xls.parse('Unit definitions').set_index('Unit')
        residents = xls.parse('Parameters').set_index('Resident_ID')
        
    data = {
        'Units': units,
        'Residents': residents}
    return data

# Declare a Model

def create_model(data):
    """create pyomo abstract model"""

    # Make the model
    model = pyomo.AbstractModel()    # creates an abstract model
    model.name = "Resident Scheduling Model"  # sets the model name 
    model.model.data = model.data  # assigns model model.data

    # Define sets
    model.Y = pyomo.Set(initialize=model.model.data["Residents"]["Year_Level"].values.unique())  # set of resident years
    model.R = pyomo.Set(initialize=model.model.data["Residents"].index.values)  # set of residents
    model.U = pyomo.Set(initialize=model.model.data["Units"].index)  # set of units
    model.Ri = pyomo.Set(initialize=model.model.data["Residents"]["Year_Level"])
    model.Theta = pyomo.Set(initialize="MICU_D,MICU_N,Twig,OPD")  # Critical units



    # Define parameters

    lst = []
    # making a set of tuples for min and max duration
    for i, j in zip(model.data["Units"]["Duration_Min"].values, model.data["Units"]["Duration_Max"].values):
        lst.append((i, j))
    

    model.Lambda = pyomo.Param(model.U, within=(lst))  # number of weeks for each unit

    lst = []
    for i, j, k, l, m, n in zip(
        model.data["Units"]["R1Min"].values,
        model.data["Units"]["R1Max"].values,
        model.data["Units"]["R2Min"].values,
        model.data["Units"]["R2Max"].values,
        model.data["Units"]["R3Min"].values,
        model.data["Units"]["R3Max"].values):
        lst.append((i, j, k, l, m, n))

    model.Phi = pyomo.Param(model.U, within=(lst))  # min residents of year i

# Solve the problem

opt = SolverFactory("glpk")
instance = model.create_instance()
instance.display()
