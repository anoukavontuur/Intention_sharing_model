from mesa.discrete_space import CellAgent
from pathfinding import Pathspace, spacetime_A_star_path
from conflict_detection import has_conflict

class VesselAgent(CellAgent):
    def __init__(self, model, start_cell, goal_cell, start_velocity, tokens):
        super().__init__(model)
        self.cell = start_cell
        self.goal = goal_cell
        self.state = ((self.cell.coordinate), self.model.time)  # (x, y), t
        self.velocity = start_velocity
        self.movement_buffer = 0

        self.path = spacetime_A_star_path(self.model.gridgraph, self.state, self.goal.coordinate)
        print(f"Vessel {self.unique_id} initial path: {self.path}")

        self.tokens = tokens
        self.offered_tokens = 0

    def update_state(self):
        self.state = ((self.cell.coordinate), self.model.time)
    
    def set_pathspace(self):
        self.pathspace = Pathspace(self.model.gridgraph, self.state, self.goal.coordinate)
    
    def cost(self, path):
        return len(path)

    def generate_alternative_path(self, opponent_offer):
        return spacetime_A_star_path(self.model.gridgraph, self.state, self.goal.coordinate, opponent_offer) 

    def wait_path(self):
        (x, y) = self.state[0]
        t = self.state[1]
        wait_step = ((x, y), t + 1)
        continue_path = spacetime_A_star_path(self.model.gridgraph, wait_step, self.goal.coordinate)
        return [wait_step] + continue_path

        
    def move_along_path(self):
        current_time = self.model.time

        if not self.path:
            return  # No path to follow

        for i, step in enumerate(self.path):
            if step[1] == current_time:
                (x, y) = step[0]
                target_cell = self.model.grid[(x, y)]
                self.cell = target_cell
                self.path = self.path[i:]
                break


    def detect_collision(self, radius):
        """Detect nearby vessels and check for planned conflicts using space-time paths."""
        self.collision_agents = []

        # Check for nearby agents
        self.nearby_agents = [
            nearby_agent
            for cell in self.cell.get_neighborhood(radius=radius)
            for nearby_agent in cell.agents
            if nearby_agent is not self
        ]
        
        # Collision detection based on planned paths (space-time)
        for nearby_agent in self.nearby_agents:
            if has_conflict(self.path, nearby_agent.path):
                print(f"\nCollision detected between Vessel {self.unique_id} and Vessel {nearby_agent.unique_id}")
                self.collision_agents.append(nearby_agent)
                return True
            
        return False

    def make_offer(self, opponent_offer):
        alt_path = self.generate_alternative_path(opponent_offer)

        if alt_path == []:
            self.path = self.wait_path()
            return "wait", self.path
       
        if self.cost(self.path) < self.cost(alt_path):
            if self.tokens - self.offered_tokens > 0:
                self.offered_tokens += 1
                return "keep", self.path
            else:
                self.path = self.pathspace.get()
                self.offered_tokens = 0
                return "change", self.path
            
        else:
            self.path = alt_path
            return "accept", self.path
    


