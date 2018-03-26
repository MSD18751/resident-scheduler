import pyomo.environ as pyomo
from pyomo.opt import SolverFactory
import pandas as pd

# ---Create a solver---
opt = SolverFactory("glpk")

# ---Define a model---
model = pyomo.AbstractModel() # creates an abstract model

# ---Define sets---
#model.Y = pyomo.Set()   # a set of year levels
model.R = pyomo.Set()   # a set of residents
#model.R_i = pyomo.Set() # set of residents of year i
model.C = pyomo.Set()   # set of clinic units
#model.G = pyomo.Set()   # clinic rotational groups 
model.T = pyomo.Set()   # a set of weeks
#model.V = pyomo.Set()   # vacation unit
model.A = pyomo.Set()   # ambulatory care units
#model.I = pyomo.Set()   # inpatient care units
#model.E = pyomo.Set()   # elective units
#model.H_u = pyomo.Set() # resident year needed for unit u 
model.U = model.C | model.A   # set of units
#model.Q = pyomo.Set()   # units requiring a group every week
#model.N = pyomo.Set()   # night shift rotations
#model.theta = pyomo.Set()   # subset considered for pahse 1
#model.S = pyomo.Set()   # standby unit
model.P = pyomo.Set()   # a set of the types of the rotation policies
model.Q = pyomo.Set()

# ---Define parameters---
model.psi = pyomo.Param(model.R, model.T) # the vacation preference of resident r for week t
model.naught_p = pyomo.Set(initialize = 1)
model.s = pyomo.Set(initialize = 1)
# model.naught_p = pyomo.(model.P) # the number of weeks between clinical rotations
#model.s = pyomo.Param(model.P) # the number of weeks a clinical rotation lasts
model.alpha_dict = {}
model.alpha_dict[("Clinic1", "min")] = 2
model.alpha_dict[("Clinic2", "min")] = 2

# ---Define variables---
model.X = pyomo.Var(model.R, model.U, model.T, domain = pyomo.Binary)    # resident r does/doesn't work unit u week t
model.W = pyomo.Var(model.R, model.U, model.T, domain = pyomo.Binary)    # resident r does/doesn't START rotation unit u week t
model.delta = pyomo.Var(model.U, model.T, domain = pyomo.Binary)    # unit u does/doesn't START a rotation in week t

# ---Define objective function---
def obj(model): # objective to satisfy resident vacation preferences
    return sum(model.X[r,u,t] * model.psi[r,t] for r in model.R for u in model.U for t in model.T)

model.obj = pyomo.Objective(rule = obj, sense = pyomo.maximize)    # a maximization problem of the function defined above

# ---Define constraints---
def Cons14(model, t, u):
    return 1 <= sum(model.X[r,u,t] for r in model.R) <= 3    # make sure at least 2 residents are working unit u every week

model.Residents = pyomo.Constraint(model.T, model.U, rule = Cons14)    # the assignment constraint for number of residents working

def Cons15(model, t, r):
    return sum(model.X[r,u,t] for u in model.U) <= 1 # makes sure that every resident is assign to max 1 place each week

model.NoClones = pyomo.Constraint(model.T, model.R, rule = Cons15)

def Cons9(model, t, r, c):
    return sum(model.X[r,c,t + (q * 1)]for q in model.Q) >= model.alpha_dict[(c,"min")] * model.W[r,c,t]
        #list(range(model.alpha_dict[(c,"min")]+1))) # Establishes rotation policy

    #return sum(model.X[r,c,min(t + q * (model.naught_p+model.s), model.np)]for q in model.Q) >= model.alpha_dict[(c,"min")] * model.W[r,c,t]

model.ClinicRotation = pyomo.Constraint(model.T, model.R, model.C, rule = Cons9)

#def Cons9(model, t, r, c):
 #   return sum(model.X[r,c,min(t+q(model.naught_p+model.s),model.np)] 
  #  >= model.alpha_dict[c,min] * model.W[r,c,t] for q in range(model.alpha_dict[c,min])) # Establishes rotation policy

#model.ClinicRotation = pyomo.Constraint(range(model.naught_p + model.s), model.R, model.C, rule = Cons9)

# ---Create an instance---
instance = model.create_instance("Feb18.dat")
results = opt.solve(instance)
instance.display()