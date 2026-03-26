import mesa
from mesa.experimental.continuous_space import ContinuousSpace 
from agents import VesselAgent

class IntentionSharingModel(mesa.Model):
    """A model for pathfinding with an intention sharing mechanism"""

    def __init__(self, n_vessels=2, rng=None, space_size=None):
        # Intitialize attributes parent class
        super().__init__(rng=rng)

        # Variables
        self.n_vessels = n_vessels
        self.space = ContinuousSpace(space_size, torus=False)    

        self.vessels = VesselAgent.create_agents(self, self.space, self.n_vessels)

    def step(self):
        pass