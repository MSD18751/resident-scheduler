# Hello World for PYOMO (Solution should be x=100)
# This PYOMO file corresponds to the following linear program
# mazimize z=x
# ST
# x<=100
# x>=0

from pyomo.environ import *  # importing PYOMO modeling objects

# creating the model object
model = ConcreteModel()

# declaring the decision variables
model.x = Var(within=NonNegativeReals)

# declaring the objective function
model.maximizeZ = Objective(expr=model.x, sense=maximize)

# declaring the constraints
model.Constraint1 = Constraint(expr=model.x <= 100)  # x can't be more than 100
