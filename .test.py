from Grid import GridGraph
from pathfinding import Pathspace, spacetime_A_star_path

class TestAgent():
    def __init__(self, start_state, goal_xy):
        self.start_state = start_state
        self.goal_xy = goal_xy
        self.path = []
    
    def set_pathspace(self, graph):
        self.pathspace = Pathspace(graph, self.start_state, self.goal_xy)
        
    def set_path(self):
        self.path = self.pathspace.path()

    def generate_alternative_path(self, graph, reservation_table):
        self.path = spacetime_A_star_path(graph, self.start_state, self.goal_xy, reservation_table)

def detect_conflicts(path1, path2):
    for step1 in path1:
        for step2 in path2:
            if step1 == step2:
                print(f"Conflict at time step {step1[1]} on cell {step1[0]}!")
                return True 
    return False

Mygraph = GridGraph(5, 5)

Agent1 = TestAgent(((0, 0), 0), (4, 4))
Agent1.set_pathspace(Mygraph)
Agent1.set_path()
print(f"Agent 1 path: {Agent1.path}")

Agent2 = TestAgent(((4, 0), 0), (0, 4))
Agent2.set_pathspace(Mygraph)
Agent2.set_path()
print(f"Agent 2 path: {Agent2.path}")

if detect_conflicts(Agent1.path, Agent2.path): 
    Agent1.generate_alternative_path(Mygraph, reservation_table=Agent2.path)

detect_conflicts(Agent1.path, Agent2.path)





