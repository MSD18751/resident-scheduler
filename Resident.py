from pyomo.environ import *
from pyomo.opt import SolverFactory
# Create a solver
opt = SolverFactory(’glpk’)

#declare model
model = AbstractModel ()

#declare sets
model.y = set()      #residency years
model.r = set()      #set of residents
model.r_i = set()    #set of residents of year i
model.c = set()      #set of clinic units
model.g = set()      #clinic rotational groups 
model.t = set()      #set of weeks
model.v = set()      #vacation unit
model.a = set()      #ambulatory care units
model.i = set()      #inpatient care units
model.e = set()      #elective units
model.h_u = set()    #resident year needed for unit u 
model.u = set()      #set of units
model.q = set()      #units requiring a group every week
model.n = set()      #night shift rotations
model.theta = set () #subset considered for pahse 1
model.s = set()      #standby unit
model.p = set()      #clinic rotational policy

#parameters
model.phi_p = param(model.p)

#decision variables
 model.x = var(model.r, model.u, model.t, within = binary) #1 if resident r rotates in unit u in week t; 0 otherwise
 model.w = var(model.r, model.u, model.t, within = binary) #1 if resident r starts a rotation in unit u in week t; 0 otherwise
 model.delta = var(model.u, model.t, within = binary)      #1 if unit u begins a rotation in week t

 
#Objective Functions

def 



