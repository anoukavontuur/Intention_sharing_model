#Agent parameters [start_cell, goal_cell, start_heading, start_velocity, tokens]
agents = [
    [(0, 0),    (29, 29),   2,  1,  1], 
    [(29, 0),   (0, 29),    0,  1,  1],
    [(6, 0),    (6, 29),    1,  1,  1],
    [(0, 25),   (29, 25),   3,  1,  1],
]

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