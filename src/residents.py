import pyomo.environ as pyomo

# ---Define a model---
model = pyomo.AbstractModel() # creates an abstract model

# ---Define sets---
model.R = pyomo.Set() # a set of residents
model.U = pyomo.Set() # a set of units
model.T = pyomo.Set() # a set of weeks

# ---Define parameters---
model.V = pyomo.Param(model.R, model.T) # the vacation preference of resident r for week t

# ---Define variables---
model.X = pyomo.Var(model.R, model.U, model.T, domain = pyomo.Binary, initialize=0)    # resident r does/doesn't work week t

# ---Define objective function---
def obj(model): # objective to satisfy resident vacation preferences
    return sum(model.X[r,u,t] * model.V[r,t] for r in model.R for u in model.U for t in model.T)

model.obj = pyomo.Objective(rule = obj, sense = pyomo.minimize)    # a minimization problem of the function defined above

# ---Define constraints---
def Cons1(model, u):
    return sum(model.X[r,u,t] for r in model.R for t in model.T) >= 2    # make sure at least 2 residents are working unit A every week

model.ResidentsA = pyomo.Constraint(model.U, rule = Cons1)    # the assignment constraint for number of residents working

def Cons3(model, t, r):
    return sum(model.X[r,u,t] for u in model.U) <= 1 # makes sure that every resdient is assign to 1 place each week

def Cons2(model, r, u):
    return sum(model.X[r,u,t] for t in model.T) <= 4

def Cons4(model, u, t):
    return sum(model.X[r, u, t] for r in model.R) <= 4

def Cons5(model, r):
    return sum(model.X[r, u, t] for u in model.U for t in model.T) >= 12 

model.vacay = pyomo.Constraint(model.R, rule=Cons5)
model.busy = pyomo.Constraint(model.U, model.T, rule=Cons4)
model.workit = pyomo.Constraint(model.R, model.U, rule=Cons2)
model.NoClones = pyomo.Constraint(model.T, model.R, rule = Cons3)