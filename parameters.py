#Vessel parameters
number_of_vessels = 4
start_positions = [(0, 0), (29, 0), (6, 0), (0, 25)]
goal_positions = [(29, 29), (0, 29), (6, 29), (29, 25)]
start_headings = [2, 0, 1, 3]
start_velocities = [1, 1, 1, 1]
tokens = [1, 1, 1, 1]

#Detection radius
detection_radius = 5

# Grid dimensions
width = 30 
height = 30

# Pathfinding parameters
v_optimal = 2        
w_distance = 0.1       
w_velocity = 0.1         
w_acceleration = 0.8  

# A* parameters
    
w_distance = 0.5       
w_velocity = 1      
w_acceleration = 1.0   