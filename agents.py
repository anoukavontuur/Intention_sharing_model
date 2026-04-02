from mesa.discrete_space import CellAgent
from pathfinding import A_star_search, reconstruct_path

class VesselAgent(CellAgent):
    def __init__(self, model, start_cell, goal_cell, start_velocity):
        super().__init__(model)
        self.cell = start_cell
        self.velocity = start_velocity
        self.start_cell = start_cell.coordinate
        self.goal_cell = goal_cell.coordinate
        self.path = []

    def set_path(self):
        came_from = A_star_search(self.model.GridGraph, self.start_cell, self.goal_cell)
        self.path = reconstruct_path(came_from, self.start_cell, self.goal_cell)

    def move_along_path(self):
        if not self.path or len(self.path) <= 1:
            return

        if not hasattr(self, "movement_buffer"):
            self.movement_buffer = 0

        self.movement_buffer += self.velocity

        while self.movement_buffer >= 1 and len(self.path) > 1:
            next_cell = self.path[1]
            self.cell = self.model.grid[next_cell]
            self.path.pop(0)
            self.movement_buffer -= 1
    
    def say_hi(self):
        print(f"Hi, I'm agent {self.unique_id} on cell {self.cell.coordinate}!")

