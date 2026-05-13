#Agent parameters [start_cell, goal_cell, start_heading, start_velocity, tokens]
agents = [
    [(1, 10),  (18, 10),  2,  2,  1],
    [(18, 10), (1, 10),   4,  2,  1],
    [(10, 1),  (10, 18),  1,  2,  1],
    [(10, 18), (10, 1),   3,  2,  1],
    [(1, 1),   (18, 18),  2,  1,  1]
]

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
 