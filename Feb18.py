import pyomo.environ as pyomo
from pyomo.opt import SolverFactory
import pandas as pd

# ---Create a solver---
opt = SolverFactory("glpk")

# ---Define a model---
model = pyomo.AbstractModel() # creates an abstract model

# ---Define sets---
model.R = pyomo.Set() # a set of residents
model.U = pyomo.Set() # a set of units
model.T = pyomo.Set() # a set of weeks

# ---Define parameters---
model.V = pyomo.Param(model.R, model.T) # the vacation preference of resident r for week t

# ---Define variables---
model.X = pyomo.Var(model.R, model.U, model.T, domain = pyomo.Binary)    # resident r does/doesn't work week t

# ---Define objective function---
def obj(model): # objective to satisfy resident vacation preferences
    return sum(model.X[r,u,t] * model.V[r,t] for r in model.R for u in model.U for t in model.T)

model.obj = pyomo.Objective(rule = obj, sense = pyomo.minimize)    # a minimization problem of the function defined above

# ---Define constraints---
def Cons1(model, t):
    return sum(model.X[r,"A",t] for r in model.R) == 2    # make sure at least 2 residents are working unit A every week

model.ResidentsA = pyomo.Constraint(model.T, rule = Cons1)    # the assignment constraint for number of residents working

def Cons2(model, t):
    return sum(model.X[r,"B",t] for r in model.R) == 2    # make sure at least 2 residents are working unit B every week

model.ResidentsB = pyomo.Constraint(model.T, rule = Cons2)    # the assignment constraint for number of residents working

def Cons3(model, t, r):
    return sum(model.X[r,u,t] for u in model.U) <= 1 # makes sure that every resdient is assign to 1 place each week

model.NoClones = pyomo.Constraint(model.T, model.R, rule = Cons3)

# ---Create an instance---
instance = model.create_instance("Feb18.dat")
results = opt.solve(instance)
instance.display()