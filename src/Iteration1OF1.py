#Declare Objective Function to Minimize the Number of Drivers
model.MinimizeDrivers = Objective(expr = model.x0 + model.x4 + model.x8 + model.x12 + model.x16 + model.x20, sense=minimize)