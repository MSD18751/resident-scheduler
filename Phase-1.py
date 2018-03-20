import pandas as pd
import pyomo.environ as pyomo
import numpy as np
from pyomo.opt import SolverFactory


def read_excel(filename):
    """Read special Excel spreadsheet to input dict.
    
    Args:
        filename: path to a spreadsheet file
        
    Returns
        dictionary of DataFrames, to be passed to create_model()
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
    model = pyomo.AbstractModel()  # creates an abstract model
    model.name = "Resident Scheduling Model"  # sets the model name 
    model.data = data  # assigns model model.data

    # Define sets
    model.Y = pyomo.Set(initialize=model.data["Residents"]["Year_Level"].unique())  # set of resident years
    model.R = pyomo.Set(initialize=model.data["Residents"].index.values)  # set of residents
    model.U = pyomo.Set(initialize=model.data["Units"].index)  # set of units
    model.Ri = pyomo.Set(initialize=model.data["Residents"]["Year_Level"])
    model.Theta = pyomo.Set(initialize=("MICU_D", "MICU_N", "Twig", "OPD"))  # Critical units



    # Define parameters

    lst = []

    # making a set of tuples for min and max duration
    
    lambdadict = {}
    for i in data["Units"].index:
        lambdadict.update({i: int(np.mean([model.data["Units"].loc[i]["Duration_Min"], model.data["Units"].loc[i]["Duration_Max"]]))})
    
    print(lambdadict)
    model.Lambda = pyomo.Param(model.U, initialize=lambdadict, default=0)  # number of weeks for each unit
    #print(model.Lambda)

    # p = {1: 1, 2: 4, 3: 9}
    # model.A = pyomo.Set(initialize=[1,2,3])
    # model.p = pyomo.Param(model.A, initialize=p)
    # model.x = pyomo.Var(model.A, within=pyomo.NonNegativeReals)
    #model.o = pyomo.Objective(expr=sum(model.p[i]*model.x[i] for i in model.A))
    #model.Phi = pyomo.Param(model.U, within=(lst))  # min residents of year i

    # Solve the problem

    opt = SolverFactory("glpk")
    instance = model.create_instance(data)
    instance.pprint()


def main():
    file = "sample_data/DataFile.xlsx"
    model_data = read_excel(file)
    create_model(model_data)

main()