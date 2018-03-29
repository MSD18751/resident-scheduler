import pandas as pd
import pyomo.environ as pyomo
import numpy as np
from pyomo.opt import SolverFactory

def read_excel(filename):
    """Read special Excel spreadsheet to input dict.
    
    Args:
        filename: path to a spreadsheet file
        
    Returns
        dictionary of DataFrames, to be passed to create_model()
    """
    with pd.ExcelFile(filename) as xls:
        units = xls.parse('Unit definitions').set_index('Unit')
        residents = xls.parse('Parameters').set_index('Resident_ID')
        history = xls.parse('Past').set_index('Resident_ID')
        sets = xls.parse('Sets').set_index("Clinic_Group")
        
    data = {
        'Units': units,
        'Residents': residents,
        'History': history,
        'Sets': sets}
    return data

def create_model(data, policy_type="4+1", model_np=52, model_v=1):
    """create pyomo abstract model"""

    # Make the model
    model = pyomo.AbstractModel()  # creates an abstract model
    model.name = "Resident Scheduling Model"  # sets the model name
    model.data = data  # assigns model data

    # Define sets

    # model.y is the set of resident years
    model.Y = pyomo.Set(
        initialize=model.data["Residents"]["Year_Level"].unique())
    # model.R is the set of residents
    model.R = pyomo.Set(
        initialize=model.data["Residents"].index.values)
        # define a dict to store possible year levels {1: None, 2: None, 3: None}
    Ridict = dict.fromkeys(model.data["Residents"]["Year_Level"])
    # update dict to have each key have a list referenced to it
    # {1: [], 2: [], 3: []}
    for i in Ridict:
        Ridict.update({i: []})
    # update each list in the dict to contain the students in each year
    # {1: [1, 2, ..., 19], 2: [20, 21, ..., 38], 3: [39, 40, ..., 57]}
    for i in model.data["Residents"].index.values:
        Ridict[model.data["Residents"].iloc[i-1]["Year_Level"]].append(i)
    # use this crazy dict to initialize Ri the set of residents in each year
    model.Ri = pyomo.Set(model.Y, initialize=Ridict)
    # model.C is the set of clinical units
    model.C = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Clinic'").index.values)
    # model.G is the clinic rotational groups
    model.G = pyomo.Set(
        initialize=model.data["Residents"]["Clinic_Groups"].unique())
    # model.T is the number of weeks (n) we're scheduling (1, 2, 3, ..., n+1)
    # the n+1 bit means you need an extra one to end at the number you want
    model.T = pyomo.Set(initialize=range(1, model_np+1))
    # model.V is the vacation unit
    model.V = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Vacation'").index.values) 
    # model.A is the set of ambulatory units
    model.A = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Ambulatory'").index.values)
    # model.I is the set of Inpatient units
    model.I = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Inpatient'").index.values) 
    # model.E is the set of elective units
    model.E = pyomo.Set(
        initialize=model.data["Units"].query(
            "Unit_type == 'Elective'").index.values)  

    # model.U is the set of all units as a union of A, C, E, I, and V
    model.U = model.A | model.C | model.E | model.I | model.V
    # define a dict for Hu
    H_u_dict = dict.fromkeys(model.data["Units"].index)
    # make each key in the dict a list and add years accepted
    for i in H_u_dict:
        H_u_dict.update({i: []})
        if (model.data["Units"].loc[[i], ["R1Min"]].values >= 1):
            H_u_dict[i].append(1)
        if (model.data["Units"].loc[[i], ["R2Min"]].values >= 1):
            H_u_dict[i].append(2)
        if (model.data["Units"].loc[[i], ["R3Min"]].values >= 1):
            H_u_dict[i].append(3)
    # use that dict to define model.H
    # which is the set of residents allowed for each unit
    model.H_u = pyomo.Set(model.U, initialize=H_u_dict)
    # model.Q is the subset of sets that have to have a rotation every week
    model.Q = pyomo.Set(
        within=model.U,
        initialize=model.data["Units"].query(
            "Student_Req == 'Yes'").index.values)
    # model.N is the subset of units that are night shifts
    model.N = pyomo.Set(
        within=model.U,
        initialize=model.data["Units"].query(
            "Day_Night == 'Night'").index.values)
    # model.Theta is the subset of units solved for in round 1
    model.Theta = pyomo.Set(
        within=model.U,
        initialize=model.data["Units"].query(
            "round_1 == 'Yes'").index)
    # model.S is the standby unit
    model.S = pyomo.Set()
    # model.P is the clinic protational policy
    P = list(["4+1", "8+2", policy_type])
    model.P = pyomo.Set(initialize=P)

    # Define parameters
    
    # model.naught_p is the num of weeks before a resident has to return to a clinic
    naught_p = {}
    for p in P:
        naught_p[p] = int(str(p).split("+")[1])
    model.naught_p = pyomo.Param(model.P, initialize=naught_p)
    # model.s is the number of rotations in the first model.phi + s weeks
    s = int(policy_type.split("+")[1])
    model.s = pyomo.Param(initialize=s)
    # model.h_g_c is 1 if group g is assigned to group C, 0 otherwise
    h_g_c_dict = {}
    for g in model.data["Sets"].index.values:
        for c in list(data["Units"].query("Unit_type == 'Clinic'").index.values):
            if model.data["Sets"].loc[g, "Clinic"] == c:
                h_g_c_dict[(g,c)] = 1
            else:
                h_g_c_dict[(g,c)] = 0 
    model.h_g_c = pyomo.Param(model.G, model.C, initialize=h_g_c_dict)
    I_r_g_dict = {}
    for r in model.data["Residents"].index.values:
        for g in model.data["Residents"]["Clinic_Groups"].unique():
            if model.data["Residents"].iloc[r-1]["Clinic_Groups"] == g:
                I_r_g_dict[r, g] = 1
            else:
                I_r_g_dict[r, g] = 0
    # model.I_r_g_dict is 1 if the resident is in unit g 0 otherwise
    model.I_r_g = pyomo.Param(model.R, model.G, initialize=I_r_g_dict)
    # model_alpha is the min and max rotation duration for each unit
    model_alpha_u = {}
    # model_zeta is the min and max number of weeks neede for 3 years
    model_zeta_u = {}
    for u in data["Units"].index.values:
        model_alpha_u[(u, "min")] = model.data["Units"].loc[u, "Weeks_Min"]
        model_alpha_u[(u, "max")] = model.data["Units"].loc[u, "Weeks_Max"]
        model_zeta_u[(u, "min")] = 3 * model.data["Units"].loc[u, "Weeks_Min"]
        model_zeta_u[(u, "max")] = 3 * model.data["Units"].loc[u, "Weeks_Max"]
    # making a set of tuples for min and max duration
    lambdadict = {} 
    lambdalst = []
    for i in data["Units"].index:
        lambdadict.update({i: int(np.mean(
            [model.data["Units"].loc[i]["Duration_Min"],
                model.data["Units"].loc[i]["Duration_Max"]]))})
        lambdalst.append(int(np.mean(
            [model.data["Units"].loc[i]["Duration_Min"],
                model.data["Units"].loc[i]["Duration_Max"]])))
    # model.Lambda is the number of weeks for each unit
    model.Lambda_u = pyomo.Param(model.U, initialize=lambdadict, default=0)
    # model_Phi_y_u is the number of year y residents needed to
    # schedule a rotation in unit u
    model_Phi_y_u = {}
    for y in list(model.data["Residents"]["Year_Level"].unique()):
        for u in model.data["Units"].index:
            for i in list(("Min", "Max")):
                model_Phi_y_u[(y, u, i)] = model.data["Units"].loc[u, str("R"+str(y)+i)]
    # model.tau is the min number of roataions
    tau = (model_np/(naught_p[policy_type]+s))
    model.tau = pyomo.Param(initialize=tau)
    # model.omega_r_u is the amount of time each returning resident
    # has been in each unit already
    omega_r_u_dict = {}
    for r in model.data["History"].index.values:
        for u in list(model.data["History"].columns):
            omega_r_u_dict[(r, u)] = model.data["History"].loc[r, u]
    model.omega_r_u = pyomo.Param(
        model.R, model.U, initialize=omega_r_u_dict, default=0)
    # model.v is the min number of weeks between the end of a vacation and
    # the next vacation block for a resident (default=1 so they don't overlap)
    model.v = pyomo.Param(initialize=model_v)
    # model.m is the min number of residents needed to run the clinical units
    m = 0
    for u in model.data["Units"].query("Unit_type == 'Clinic'").index:
        for y in model.data["Residents"]["Year_Level"].unique():
            m = m + model.data["Units"].loc[u, str("R"+str(y)+"Min")]
    model.m = pyomo.Param(initialize=m)
    # model.psi_r_t is the vacation preferences of each resident for each week
    psi_r_t_dict = {}
    for r in model.data["Residents"].index.values:
        for t in range(1, model_np+1):
            psi_r_t_dict[(r, t)] = model.data["Residents"].loc[
                (r, str("Week_" + str(t)))]
    model.psi_r_t = pyomo.Param(model.R, model.T, initialize=psi_r_t_dict)

    # ---Define variables---
    model.X = pyomo.Var(model.R, model.U, model.T, domain = pyomo.Binary)    # resident r does/doesn't work unit u week t
    model.W = pyomo.Var(model.R, model.U, model.T, domain = pyomo.Binary)    # resident r does/doesn't START rotation unit u week t
    model.delta = pyomo.Var(model.U, model.T, domain = pyomo.Binary)    # unit u does/doesn't START a rotation in week t

    # ---Define objective function---
    def obj(model): # objective to satisfy resident vacation preferences
        return sum(model.X[r,u,t] * model.psi_r_t[r,t] for r in model.R for u in model.U for t in model.T)

    model.obj = pyomo.Objective(rule = obj, sense = pyomo.maximize)    # a maximization problem of the function defined above

    # ---Define constraints---
    def Cons9(model, r, c, t):
        for r in model.R:
            for c in model.C:
                for t in list(range(1,model.naught_p[policy_type] + model.s + 1)):
                    sumofX = 0
                    q = 0
                    while t + (q * (model.naught_p[policy_type] + model.s)) <= model_np:
                         sumofX = sumofX + model.X[r,c,t + (q * (model.naught_p[policy_type] + model.s))]
                         q = q + 1
                    return sumofX >= model_alpha_u[(c,"min")] * model.W[r,c,t]

    model.ClinicRotation = pyomo.Constraint(model.R, model.C, list(range(1, naught_p[policy_type] + s + 1)), rule = Cons9)

    def Cons10(model, r, c):
        for r in model.R:
            for c in model.C:
                sumofX = 0
                t = 1
                while t <= (model.naught_p[policy_type] + model.s):
                    sumofX = sumofX + model.X[r,c,t]
                    t = t + 1
                return sumofX == 1

    model.FirstClinic = pyomo.Constraint(model.R, model.C, rule = Cons10)
    
    def Cons11(model, r, t, c, g):
        return sum(sum(model.I_r_g[r,g] * model.h_g_c[g,c] * model.W[r,c,t] for g in model.G) for r in model.R) >= model.m

    model.ClinicVerification = pyomo.Constraint(model.R, model.T, model.C, model.G, rule = Cons11)

    def Cons14(model, t, u):
        return model_Phi_y_u[(y, u, "Min")] <= sum(model.X[r,u,t] for r in model.R) <= model_Phi_y_u[(y, u, "Max")]    # make sure at least 2 residents are working unit u every week

    model.Residents = pyomo.Constraint(model.T, model.U, rule = Cons14)    # the assignment constraint for number of residents working

    def Cons15(model, r, t):
        return sum(model.X[r,u,t] for u in model.U) <= 1 # makes sure that every resident is assign to max 1 place each week

    model.NoClones = pyomo.Constraint(model.R, model.T, rule = Cons15)

    def Cons16(model, r, u, t):
        return sum(model.X[r, u, t] for u in model.U and not model.H_u) == 0
    model.NoYoungFolks = pyomo.Constraint(model.Ri, model.U, model.T, rule = Cons16)

    # Solve the problem
    opt = SolverFactory("glpk")
    instance = model.create_instance(data)
    # instance.pprint()
    results = opt.solve(instance)
    instance.display()

def main():
    file = "sample_data/DataFile.xlsx"
    model_data = read_excel(file)
    create_model(data=model_data, policy_type="4+1")

main()