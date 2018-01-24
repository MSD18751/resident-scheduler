from pyomo.environ import *
from pyomo.opt import SolverFactory
# Create a solver
opt = SolverFactory(’glpk’)

# Declare model
model = AbstractModel()

# Declare sets
Y = set()      # residency years
R = set()      # set of residents
R_i = set()    # set of residents of year i
C = set()      # set of clinic units
G = set()      # clinic rotational groups 
T = set()      # set of weeks
V = set()      # vacation unit
A = set()      # ambulatory care units
I = set()      # inpatient care units
E = set()      # elective units
H_u = set()    # resident year needed for unit u 
U = set()      # set of units
Q = set()      # units requiring a group every week
N = set()      # night shift rotations
theta = set()  # subset considered for pahse 1
S = set()      # standby unit
P = set()      # clinic rotational policy

# Parameters
pi_p = param(P[1])  # number of weeks between clinic weeks
s = param()  # number of consecutive weeks at clinic
h_gc = # groups associated to each clinic
I_rg = # residents assigned to each group
zeta_u = # weeks required in rotation u over 3 years
alpha_u = # weeks required in rotation in a year
lambda_u =  # number of consecutive weeks required in a rotation
phi_iu =  # number of residents of year i needed to work unit u
tau =  # minimum number of clinic rotations in a year
omega_ru =  # number of rotations resident r has already done in u
v = # minimum number of weeks between vacation periods
m =  # minimum number of residents required in clinic each week
psi_rt = param  # resident vacation preference


# Decision variables
x = var(r, u, t, within=binary)  # 1 if resident r rotates in unit u in week t
w = var(r, u, t, within=binary)  # 1 if resident r starts in unit u in week t
delta = var(u, t, within=binary)  # 1 if unit u begins a rotation in week t

Xtc1 = Var(within=binary)  # 1 if Taylor does Cardio Week 1
Xtc2 = Var(within=binary)  # 1 if Taylor does Cardio Week 2
Xtn1 = Var(within=binary)  # 1 if Taylor does Neuro Week 1
Xtn2 = Var(within=binary)  #1 if Taylor does Neuro Week 2

# Objective Functions
def Resident_Satisfaction(model):
    return sum(psi[r,t] * x[r,u,t] for r in R for t in T for u in V)
model.MaxResSatisfaction = Objective(rule = Resident_Satisfaction, sense = maximize)
