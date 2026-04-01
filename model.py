from agents import VesselAgent, MarkerAgent
from pathfinding import GridGraph

import mesa
from mesa.discrete_space import OrthogonalMooreGrid

class IntentionSharingModel(mesa.Model):
    def __init__(self, number_of_vessels, width, height, start_coordinate, goal_coordinate):
        super().__init__()
        self.number_of_vessels = number_of_vessels
        self.grid = OrthogonalMooreGrid((width, height), torus=False, random=self.random)
        self.GridGraph = GridGraph(width, height)

        VesselAgent.create_agents(
            self, 
            self.number_of_vessels, 
            self.grid[start_coordinate])
        
        MarkerAgent.create_agents(
            self, 
            self.number_of_vessels, 
            self.grid[goal_coordinate])
        
        self.agents_by_type[VesselAgent].do("set_goal", goal_coordinate)
    
    def step(self):
        self.agents_by_type[VesselAgent].do("say_hi")
        self.agents_by_type[VesselAgent].do("move_along_path")


