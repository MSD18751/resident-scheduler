from pyomo.environ import *
from pyomo.opt import SolverFactory
# Create a solver
opt = SolverFactory(’glpk’)

#declare model
model = AbstractModel ()

#declare sets
y = set()      #residency years
r = set()      #set of residents
r_i = set()    #set of residents of year i
c = set()      #set of clinic units
g = set()      #clinic rotational groups 
t = set()      #set of weeks
v = set()      #vacation unit
a = set()      #ambulatory care units
i = set()      #inpatient care units
e = set()      #elective units
h_u = set()    #resident year needed for unit u 
u = set()      #set of units
q = set()      #units requiring a group every week
n = set()      #night shift rotations
theta = set () #subset considered for pahse 1
s = set()      #standby unit
p = set()      #clinic rotational policy

#parameters
phi_p = param(p[1])


#decision variables
 x = var(r, u, t, within = binary) #1 if resident r rotates in unit u in week t; 0 otherwise
 w = var(r, u, t, within = binary) #1 if resident r starts a rotation in unit u in week t; 0 otherwise
 delta = var(u, t, within = binary)      #1 if unit u begins a rotation in week t

 
#Objective Functions

def 



