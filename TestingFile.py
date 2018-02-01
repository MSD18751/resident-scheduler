from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd

# Create a solver
opt = SolverFactory('glpk')

# Create a dataframe
dfsets = pd.read_excel("sample_data/DataFile.xlsx", sheet_name = "Sets")
dfparams = pd.read_excel("sample_data/DataFile.xlsx", sheet_name = "Parameters")

#print(dfsets)
#print(dfparams)

# Declare model
model = AbstractModel()


instance = model.create_instance(dfparams)
solver_results = opt.solve(instance)

# Declare sets
model.Y = Set(dfparams["Year_Level"].unique())      # residency year
print(model.Y)
model.R = Set(dfparams["Resident_ID"])      # set of residents
print(model.R)
model.R_i = Set(model.Y)    # set of residents of year i
