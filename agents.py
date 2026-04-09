from mesa.discrete_space import CellAgent
from pathfinding import spacetime_A_star_search, reconstruct_path

class VesselAgent(CellAgent):
    def __init__(self, model, start_cell, goal_cell, start_velocity):
        super().__init__(model)

        self.cell = start_cell
        self.goal = goal_cell

        self.state = ((self.cell.coordinate), self.model.time)  # (x, y), t

        self.velocity = start_velocity
        self.movement_buffer = 0

        self.plan = {}

    def change_goal(self, new_goal_cell):
        self.goal = new_goal_cell
        self.plan = {}

    def set_path(self, graph, reservation_table=None):
        came_from, goal_state = spacetime_A_star_search(
            graph,
            self.state,
            self.goal.coordinate,
            reservation_table=reservation_table,
        )

        self.plan = reconstruct_path(came_from, self.state, goal_state)
        print(f"Agent {self.unique_id} planned path: {self.plan}")
        
    def move_along_path(self):
        current_time = self.model.time

        if current_time not in self.plan:
            return  # No planned move for this timestep
        
        (x, y) = self.plan.get(current_time)
        target_cell = self.model.grid[(x, y)]
        self.plan.pop(current_time-1)
        self.cell = target_cell

    def detect_nearby_vessels(self, radius):
        """Detect nearby vessels and check for planned conflicts using space-time paths."""
        self.nearby_agents = [
            nearby_agent
            for cell in self.cell.get_neighborhood(radius=radius)
            for nearby_agent in cell.agents
            if nearby_agent is not self
        ]
        
        # Collision detection based on planned paths (space-time)
        for nearby_agent in self.nearby_agents:
            print(f"Agent {self.unique_id} detects nearby agent {nearby_agent.unique_id} at cell {nearby_agent.cell.coordinate}.")
            for step in self.planning: 
                if self.planning[step] == nearby_agent.planning[step]:
                    print(f"Agent {self.unique_id} has a potential conflict with agent {nearby_agent.unique_id} at time step {step} on cell {self.planning[step]}!")



