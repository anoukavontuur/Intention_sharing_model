from scenarios import set_scenario

#Number of runs
n_runs = 10

#Agent scenarios
scenario = 1
agents = set_scenario(scenario)
number_of_vessels = len(agents)

#Detection radius
detection_radius = 8

# Grid dimensions
width = 20 
height = 20

# Pathfinding parameters
v_optimal = 2        
w_distance = 0.2     
w_velocity = 0     
w_acceleration = 0.2

# maximum horizon
horizon = 30
 