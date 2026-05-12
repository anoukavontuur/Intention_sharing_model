#Vessel parameters
number_of_vessels = 4
start_positions = [(0, 0), (19, 0), (6, 0), (0, 15)]
goal_positions = [(19, 19), (0, 19), (6, 19), (19, 15)]
start_headings = [2, 0, 1, 3]
start_velocities = [1, 1, 1, 1]
tokens = [1, 1, 1, 1]

#Detection radius
detection_radius = 15

# Grid dimensions
width = 30 
height = 30

# Pathfinding parameters
v_optimal = 2        # preferred velocity
w_distance = 1.0       # weight for distance
w_velocity = 0.5         # penalty for wrong speed
w_acceleration = 1.0  # penalty for acceleration

# A* parameters
    
w_distance = 0.5       
w_velocity = 1      
w_acceleration = 1.0   