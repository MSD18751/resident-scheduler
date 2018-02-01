from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as import pd

# Create a solver
opt = SolverFactory(’glpk’)

#Create a dataframe
dflists = pd.read_excel("sample_data/mandatory_units_and clinic_groups.xlsx")

print(dflists)

# Declare model
model = AbstractModel()

# Declare sets
model.Y = Set(within = 1,2,3)      # residency years NOTE THIS IS HARDCODED RIGHT NOW
model.R = Set()      # set of residents
model.R_i = Set(model.Y)    # set of residents of year i
model.C = Set()      # set of clinic units
model.G = Set()      # clinic rotational groups 
model.T = Set()      # set of weeks
model.V = Set()      # vacation unit
model.A = Set()      # ambulatory care units
model.I = Set()      # inpatient care units
model.E = Set()      # elective units
model.H_u = Set()    # resident year needed for unit u 
model.U = Set()      # set of units
model.Q = Set()      # units requiring a group every week
model.N = Set()      # night shift rotations
model.theta = Set()  # subset considered for pahse 1
model.S = Set()      # standby unit
model.P = Set()      # clinic rotational policy

# Parameters
pi_p = Param(P[1])  # number of weeks between clinic weeks
s = Param()  # number of consecutive weeks at clinic
h_gc = Param()# groups associated to each clinic
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
