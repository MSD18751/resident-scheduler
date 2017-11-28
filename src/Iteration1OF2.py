#Declare Objective Function to Minimize the Number of Drivers on noon shift
model.MinimizeNoonDrivers = Objective(expr = model.x12, sense=minimize)