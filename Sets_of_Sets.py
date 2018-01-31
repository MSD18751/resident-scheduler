from pyomo.environ import *
from pyomo.opt import SolverFactory



model = AbstractModel()
# Define sets    
model.PRODUCTS = Set(ordered=True)
model.METHODS = Set()
model.REFIRING = Set(ordered=True)

# Define parameters
model.productRequirement = Param(model.PRODUCTS) 
model.percentYield = Param(model.PRODUCTS, model.REFIRING) 
model.methodYield = Param(model.PRODUCTS, model.METHODS) 

# Define decision vars

# number of times method m is run
model.M = Var(model.METHODS, within=NonNegativeReals)   
# number of product i available
model.P = Var(model.PRODUCTS, within=NonNegativeReals)
# number of times to run refiring
model.R = Var(model.REFIRING, within=NonNegativeReals)

# Objective fucntion

def objective_rule(model):
    return 50*model.M[1] + 70*model.M[2] + 25*sum(model.REFIRING[i] for i in model.REFIRING)
model.Cost = Objective(rule=objective_rule, sense=minimize)

# Constraints
def demands_rule(model, i):
    return model.P[i] >= model.productRequirement[i]
model.demands = Constraint(model.PRODUCTS, rule=demands_rule)

def amountofPD_rule(model):
    return model.P[1] == 0.3*model.M[2]+0.2*model.M[3]-model.R[1]
model.amountofPD = Constraint(rule=amountofPD_rule)

def amountofP1_rule(model):
    return model.P[1] == 0.3*model.M[1] + 0.2*model.M[2] \
        + 0.25*model.R['D']-0.7*model.R[1]
model.amountofP1 = Constraint(rule=amountofP1_rule)

def amountofP2_rule(model):
    return model.P[2] == 0.2*model.M[1]+0.25*model.M[2]+0.15*model.R[1] \
        + 0.3*model.R[1]-0.6*model.R[2]
model.amountofP2 = Constraint(rule=amountofP2_rule)

def amountofP3_rule(model):
    return model.P[3] == 0.15*model.M[1]+0.2*model.M[2]+0.2*model.R[1] \
        + 0.2*model.R[1]+0.3*model.R[2]-0.5*model.R[3]
model.amountofP3 = Constraint(rule=amountofP3_rule)

def amountofP4_rule(model, m, j):
    return P[4] == sum(model.methodYield[4, m]*model.M[m] + 
        model.percentYield[4, j]*model.R[j] 
        for m in model.METHODS for j in model.REFIRING)
model.amountofP4 = Constraint(rule=amountofP4_rule)

def kiln_rule(model, m, i):
    return sum(model.M[m]+model.R[i] <= 20000 
        for m in model.METHODS for i in model.REFIRING)
model.KilnTime = Constraint(rule=kiln_rule)
