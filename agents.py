from mesa.discrete_space import CellAgent, FixedAgent
from pathfinding import A_star_search, reconstruct_path

class VesselAgent(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
    
    def set_goal(self, goal):
        self.start = self.cell.coordinate
        self.goal = goal
        came_from, cost_so_far = A_star_search(self.model.GridGraph, self.start, self.goal)
        self.path = reconstruct_path(came_from, self.start, self.goal)
        print(f"Agent {self.unique_id} has path: {self.path}")

    def move_along_path(self):
        if self.path and len(self.path) > 1:
            next_cell = self.path[1]  # the first cell in the path is the current position
            self.cell = self.model.grid[next_cell]
            self.path.pop(0)  # remove the current position from the path

    def say_hi(self):
        print(f"Hi, I'm agent {self.unique_id} on cell {self.cell.coordinate}!")

class MarkerAgent(FixedAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell