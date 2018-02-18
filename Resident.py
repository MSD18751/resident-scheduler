from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as import pd

# Create a solver
opt = SolverFactory(’glpk’)

# Create a dataframe
dfsets = pd.read_excel("sample_data/DataFile.xlsx", sheet_name = "Sets")
dfparams = pd.read_excel("sample_data/DataFile.xlsx", sheet_name = "Parameters")

print(dfsets)
print(dfparams)

# Declare model
model = AbstractModel()

# Declare sets
model.Y = Set(dfparams[Year Level].unique())      # residency year
model.R = Set(dfparams[RESIDENT ID])      # set of residents
model.R_i = Set(model.Y)    # set of residents of year i
model.C = Set(dfsets[Units])      # set of clinic units
model.G = Set(dfsets[Clinic_Group])      # clinic rotational groups 
model.T = Set(initialize = "1,2,3,4,5,6,7,8,9,10")      # Is there a better way to do this? # set of weeks
model.V = Set("V")      # vacation unit
model.A = Set()      # ambulatory care units
model.I = Set()      # inpatient care units
model.E = Set()      # elective units
model.H_u = Set()    # resident year needed for unit u 
model.U = Set(model.A, model.I, model.E, model.V, model.C)      # set of units
model.Q = Set()      # units requiring a group every week
model.N = Set()      # night shift rotations
model.theta = Set()  # subset considered for pahse 1
model.S = Set()      # standby unit
model.P = Set()      # clinic rotational policy

# Parameters
model.pi_p = Param(P[1])  # number of weeks between clinic weeks
model.s = Param()  # number of consecutive weeks at clinic
model.h_gc = Param()# groups associated to each clinic
model.I_rg = # residents assigned to each group
model.zeta_u = # weeks required in rotation u over 3 years
model.alpha_u = # weeks required in rotation in a year
model.lambda_u =  # number of consecutive weeks required in a rotation
model.phi_iu =  # number of residents of year i needed to work unit u
model.tau =  # minimum number of clinic rotations in a year
model.omega_ru =  # number of rotations resident r has already done in u
model.v = # minimum number of weeks between vacation periods
model.m =  # minimum number of residents required in clinic each week
model.psi_rt = param  # resident vacation preference


# Decision variables
Xprime = var(r, u, t, within=binary)  # 1 if resident r rotates in unit u in week t
Wprime = var(r, u, t, within=binary)  # 1 if resident r starts in unit u in week t
deltaprime = var(u, t, within=binary)  # 1 if unit u begins a rotation in week t

# Objective Functions
def Resident_Satisfaction(model):
    return sum(psi[r,t] * x[r,u,t] for r in R for t in T for u in V)
model.MaxResSatisfaction = Objective(rule = Resident_Satisfaction, sense = maximize)


Def objective1_rule(model):
		Return sum(model.psi * model.X for r in model.R for u in model.V for t in model.T)
	model.Schedule = Objective(rule=objective1_rule, sense = maximize)
