from pyomo.environ import *
from pyomo.opt import SolverFactory
# Create a solver
opt = SolverFactory(’glpk’)

# Declare model
model = AbstractModel()

# Declare sets
y = set()      # residency years
r = set()      # set of residents
r_i = set()    # set of residents of year i
c = set()      # set of clinic units
g = set()      # clinic rotational groups 
t = set()      # set of weeks
v = set()      # vacation unit
a = set()      # ambulatory care units
i = set()      # inpatient care units
e = set()      # elective units
h_u = set()    # resident year needed for unit u 
u = set()      # set of units
q = set()      # units requiring a group every week
n = set()      # night shift rotations
theta = set()  # subset considered for pahse 1
s = set()      # standby unit
p = set()      # clinic rotational policy

# Parameters
phi_p = param(p[1])


# Decision variables
x = var(r, u, t, within=binary)  # 1 if resident r rotates in unit u in week t
w = var(r, u, t, within=binary)  # 1 if resident r starts in unit u in week t
delta = var(u, t, within=binary)  # 1 if unit u begins a rotation in week t

Xtc1 = Var(within=binary)  # 1 if Taylor does Cardio Week 1
Xtc2 = Var(within=binary)  # 1 if Taylor does Cardio Week 2
Xtn1 = Var(within=binary)  # 1 if Taylor does Neuro Week 1
Xtn2 = Var(within=binary)  #1 if Taylor does Neuro Week 2

# Objective Functions