from pathfinding import GridGraph, reconstruct_k_paths, spacetime_A_star_search

Mygraph = GridGraph(5, 5)

class TestAgent():
    def __init__(self, start_state, goal_xy):
        self.start_state = start_state
        self.goal_xy = goal_xy
    
    def plan_path(self, graph, reservation_table=None):
        self.came_from, goal_state, self.cost_so_far = spacetime_A_star_search(
            graph, 
            self.start_state, 
            self.goal_xy, 
            max_goals=5, 
            reservation_table=reservation_table
            )
        
        self.paths, self.plans = reconstruct_k_paths(
            self.came_from, 
            self.start_state, 
            goal_state, 
            self.cost_so_far
            )

Agent1 = TestAgent(((0, 0), 0), (4, 4))
Agent1.plan_path(Mygraph)

for destination, origin in Agent1.came_from.items():
    if destination[0] == (2, 2):
        print(f"From {origin} to {destination}")

for n in range(len(Agent1.plans)):
    print(f"Path {n}: {Agent1.plans[n]}")

for goal, cost in Agent1.cost_so_far.items():
    if goal[0] == (2, 2):
        print(f"Cost to reach {goal}: {cost}")


# Agent2 = TestAgent(((4, 0), 0), (0, 4))
# Agent2.plan_path(Mygraph)
# print("Planned paths for Agent 2:", Agent2.paths)



