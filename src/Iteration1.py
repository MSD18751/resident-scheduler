#Code Iteration 1

#Import pyomo
from pyomo.environ import *

#Declare Model
model = AbstractModel()

#Declare Sets
model.DriverDemand = 

#Decalre Decision Variables
model.x0 = Var(within=NonNegativeReals) #This is the number of drivers starting a shift at 0h00
model.x4 = Var(within=NonNegativeReals) #This is the number of drivers starting a shift at 4h00
model.x8 = Var(within=NonNegativeReals) #This is the number of drivers starting a shift at 8h00
model.x12 = Var(within=NonNegativeReals) #This is the number of drivers starting a shift at 12h00
model.x16 = Var(within=NonNegativeReals) #This is the number of drivers starting a shift at 16h00
model.x20 = Var(within=NonNegativeReals) #This is the number of drivers starting a shift at 20h00

#Declare Constraints
model.con1 = Constraint(expr = model.x0 + model.x20 >= 4) # This makes sure there are atleast 4 drivers working
model.con2 = Constraint(expr = model.x4 + model.x0 >= 8) # This makes sure there are atleast 8 drivers working
model.con3 = Constraint(expr = model.x8 + model.x4 >= 10) # This makes sure there are atleast 10 drivers working
model.con4 = Constraint(expr = model.x12 + model.x8 >= 7) # This makes sure there are atleast 7 drivers working
model.con5 = Constraint(expr = model.x16 + model.x12 >= 12) # This makes sure there are atleast 12 drivers working
model.con6 = Constraint(expr = model.x20 + model.x16 >= 4) # This makes sure there are atleast 4 drivers working