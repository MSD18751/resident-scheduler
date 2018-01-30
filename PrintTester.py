from pyomo.environ import *
from pyomo.opt import SolverFactory
# Create a solver
opt = SolverFactory(’glpk’)

# Declare model
model = AbstractModel()

# Declare sets
y = set(1, 2, 3)      # residency years
r = set("Dan", "Taylor", "Liam")      # set of residents
yr = set(y, r)

print(yr)