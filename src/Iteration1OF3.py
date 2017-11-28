#Declare Objective Function to Minimize the Cost
model.MinimizeCost = Objective(expr = 4 * model.x0 + 4 * model.x4 + 2 * model.x8 + 2 * model.x12 + 2 * model.x16 + 4 * model.x20, sense=minimize)