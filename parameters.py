# 3 vessels large grid
number_of_vessels = 3
start_positions = [(0, 0), (29, 0), (15, 0)]
goal_positions = [(29, 29), (0, 29), (15, 29)]
start_headings = [2, 0, 1]
start_velocities = [1, 1, 1]
tokens = [1, 1, 1]

detection_radius = 6

# Grid dimensions
width = 30 
height = 30

# Pathfinding parameters
v_optimal = 2        # preferred velocity
w_distance = 1.0       # weight for distance
w_velocity = 0.5         # penalty for wrong speed
w_acceleration = 1.0  # penalty for acceleration

