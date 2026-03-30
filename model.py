from agents import VesselAgent

import mesa
from mesa.discrete_space import OrthogonalMooreGrid

class IntentionSharingModel(mesa.Model):
    def __init__(self, number_of_vessels, width, height):
        super().__init__()
        self.number_of_vessels = number_of_vessels
        self.grid = OrthogonalMooreGrid((width, height), torus=False, random=self.random)

        agents = VesselAgent.create_agents(
            self, 
            self.number_of_vessels, 
            self.random.choices(self.grid.all_cells.cells, k=self.number_of_vessels))
    
    def step(self):
        self.agents.do("say_hi")


