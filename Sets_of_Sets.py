from pyomo.environ import *
from pyomo.opt import SolverFactory


def main():
    Model.A = Set(initialize=[1,2,3])
    Model.B = Set(initialize=[4,5,6])
    Model.C = Set(Model.A,Model.B)

    print(Model.C)

main()