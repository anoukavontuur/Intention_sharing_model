def set_scenario(scenario_number):
    if scenario_number == 1:
        #head on collision
        return [
            [(10, 1),  (10, 18),  1,  2,  1],
            [(10, 18), (10, 1),   5,  2,  1],
        ]
    elif scenario_number == 2:
        #crossing paths
        return [
            [(10, 1),  (10, 18),   1,  2,  1],
            [(1, 10),  (18, 10),   3,  2,  1],
        ]
    elif scenario_number == 3:
        #crossing paths with a third vessel
        return [
            [(10, 1),  (10, 18),   1,  2,  1],
            [(1, 10),  (18, 10),   3,  2,  1],
            [(1, 1),   (18, 18),   2,  2,  1]
        ]
    elif scenario_number == 4:
        #crowded
        return [
            [(1, 10),  (18, 10),  2,  2,  1],
            [(18, 10), (1, 10),   4,  2,  1],
            [(10, 1),  (10, 18),  1,  2,  1],
            [(10, 18), (10, 1),   3,  2,  1],
            [(1, 1),   (18, 18),  2,  1,  1]
        ]
    else:
        raise ValueError("Invalid scenario number. Please choose a number between 1 and 5.")
    
