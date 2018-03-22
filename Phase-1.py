import pandas as pd
import pyomo.environ as pyomo
import numpy as np
from pyomo.opt import SolverFactory

def makedict(dictname, query):
    """makes a dict to use for defining sets
    
    Args:
        dictname: name of dict
        query: formula to use
        
    Returns:
        dictionary with relevant keys and values for pyomo set initialization
        """

    dictname = {}



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
    model.data = data  # assigns model data

    # Define sets

    # model.y is the set of resident years
    model.Y = pyomo.Set(
        initialize=model.data["Residents"]["Year_Level"].unique())
    # model.R is the set of residents
    model.R = pyomo.Set(
        initialize=model.data["Residents"].index.values)
    # model.A is the set of ambulatory units
    model.A = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Ambulatory'").index.values)
    # model.C is the set of clinical units
    model.C = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Clinic'").index.values)
    # model.E is the set of elective units
    model.E = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Elective'").index.values)  
    # model.I is the set of Inpatient units
    model.I = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Inpatient'").index.values) 
    # model.V is the vacation unit
    model.V = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Vacation'").index.values)  
    # model.U is the set of all units as a union of A, C, E, I, and V
    model.U = model.A | model.C | model.E | model.I | model.V
    # model.N is the subset of units that are night shifts
    model.N = pyomo.Set(
        within=model.U,
        initialize=model.data["Units"].query(
            "Day_Night == 'Night'").index.values)
    # model.Theta is the subset of units solved for in round 1
    model.Theta = pyomo.Set(
        within=model.U,
        initialize=model.data["Units"].query(
            "round_1 == 'Yes'").index)
    # define a dict to store possible year levels {1: None, 2: None, 3: None}
    Ridict = dict.fromkeys(model.data["Residents"]["Year_Level"])
    # update dict to have each key have a list referenced to it
    # {1: [], 2: [], 3: []}
    for i in Ridict:
        Ridict.update({i: []})
    # update each list in the dict to contain the students in each year
    # {1: [1, 2, ..., 19], 2: [20, 21, ..., 38], 3: [39, 40, ..., 57]}
    for i in model.data["Residents"].index.values:
        Ridict[model.data["Residents"].iloc[i-1]["Year_Level"]].append(i)
    # use this crazy dict to initialize Ri the set of residents in each year
    model.Ri = pyomo.Set(model.Y, initialize=Ridict)
    # model.T is the number of weeks (n) we're scheduling (1, 2, 3, ..., n+1)
    # the n+1 bit means you need an extra one to end at the number you want
    model.T = pyomo.Set(initialize=range(1, 53))
    # model.G is the clinic rotational groups
    model.G = pyomo.Set(
        initialize=model.data["Residents"]["Clinic_Groups"].unique())
    # define a dict for Hu
    Hudict = dict.fromkeys(model.data["Units"].index)
    # make each key in the dict a list and add years accepted
    for i in Hudict:
        Hudict.update({i: []})
        if (model.data["Units"].loc[[i], ["R1Min"]].values >= 1):
            Hudict[i].append(1)
        if (model.data["Units"].loc[[i], ["R2Min"]].values >= 1):
            Hudict[i].append(2)
        if (model.data["Units"].loc[[i], ["R3Min"]].values >= 1):
            Hudict[i].append(3)
    # use that dict to define model.H
    # which is the set of residents allowed for each unit
    model.H = pyomo.Set(model.U, initialize=Hudict)
    # model.S is the standby unit
    model.S = pyomo.Set()
    # model.P is the clinic protational policy
    model.P = pyomo.Set(initialize=["4+1", "8+2"])
    # model.Q is the subset of sets that have to have a rotation every week
    model.Q = pyomo.Set(
        within=model.U,
        initialize=model.data["Units"].query(
            "Student_Req == 'Yes'").index.values)
    # Define parameters

    # making a set of tuples for min and max duration
    
    lambdadict = {}
    for i in data["Units"].index:
        lambdadict.update({i: int(np.mean([model.data["Units"].loc[i]["Duration_Min"], model.data["Units"].loc[i]["Duration_Max"]]))})
    model.Lambda = pyomo.Param(model.U, initialize=lambdadict, default=0)  # number of weeks for each unit

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