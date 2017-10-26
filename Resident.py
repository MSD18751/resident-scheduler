from pyomo.environ import *
from pyomo.opt import SolverFactory
# Create a solver
opt = SolverFactory(’glpk’)

#declare model
model = AbstractModel ()

#declare sets
model.r = set() #set of residents
model.u = set() #set of units
model.t = set() #set of weeks

#decision variables
 model.x = var(model.r, model.u, model.t, within = binary) #1 if resident r rotates in unit u in week t; 0 otherwise
 model.w = var(model.r, model.u, model.t, within = binary) #1 if resident r starts a rotation in unit u in week t; 0 otherwise
 model.delta = var(model.u, model.t, within = binary)      #1 if unit u begins a rotation in week t

 




