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
        self.movement_buffer = 0

    def set_path(self):
        came_from = A_star_search(self.model.GridGraph, self.start_cell, self.goal_cell)
        self.path = reconstruct_path(came_from, self.start_cell, self.goal_cell)
        print(f"Set path for agent {self.unique_id}")

    def planning_horizon(self):
        self.planning = {}
        buffer = self.movement_buffer
        path_index = 0
        self.planning[0] = self.cell.coordinate

        for step in range(1, 5):
            buffer += self.velocity

            while buffer >= 1 and path_index + 1 < len(self.path):
                buffer -= 1
                path_index += 1

            self.planning[step] = self.path[path_index]

    def detect_nearby_vessels(self, radius):
        self.nearby_agents = [
            nearby_agent
            for cell in self.cell.get_neighborhood(radius=radius)
            for nearby_agent in cell.agents
            if nearby_agent is not self
        ]
        
        #Collision detection based on planned paths
        if len(self.nearby_agents) > 0:
            for nearby_agent in self.nearby_agents:
                print(f"Agent {self.unique_id} detects nearby agent {nearby_agent.unique_id} at cell {nearby_agent.cell.coordinate}.")
                for step in self.planning: 
                    if self.planning[step] == nearby_agent.planning[step]:
                        print(f"Agent {self.unique_id} has a potential conflict with agent {nearby_agent.unique_id} at time step {step} on cell {self.planning[step]}!")

                


    def move_along_path(self):
        self.movement_buffer += self.velocity

        while self.movement_buffer >= 1 and len(self.path) > 1:
            next_cell = self.path[1]
            self.cell = self.model.grid[next_cell]
            self.path.pop(0)
            self.movement_buffer -= 1
    
    def say_hi(self):
        print(f"Hi, I'm agent {self.unique_id} on cell {self.cell.coordinate}!")

