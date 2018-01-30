#OJ Juice Company Abstract Model
from pyomo.environ import *

#declare model
model = AbstractModel ()

#Sets
model.Quality = Set ()
model.Products = Set ()

#Parameters
model.Quantity = Param (model.Quality)
model.Profit = Param (model.Products)

#Decision variables
model.X = Var(model.Quality,model.Products, within = NonNegativeReals)

#Objective function
def objective_rule(model):
    return sum (model.Profit[j]*model.X[i,j] for i in model.Quality for j in model.Products)
model.TotalProfit = Objective (rule=objective_rule, sense = maximize)

def oranges_rule (model, i):
    return (sum (model.X[i,j] for j in model.Products) <=model.Quantity[i])
model.available_oranges = Constraint(model.Quality,rule=oranges_rule)

def quality_1_rule (model):
    return (-2*model.X[6,'juice']+1*model.X[9,'juice'] >= 0)
model.quality_juice = Constraint(rule=quality_1_rule)

def quality_2_rule (model):
    return((-1*model.X[6,'bags']+2*model.X[9,'bags']) >=0)
model.quality_bags = Constraint(rule=quality_2_rule)

# code to solve the model
# pyomo solve --solver=glpk ojModel.py ojData.dat --summary>>ojResults.txt
