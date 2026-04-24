from agents import VesselAgent
from pathfinding import GridGraph
import parameters as p
from negotiation import negotiate

import mesa
from mesa.discrete_space import OrthogonalMooreGrid

class IntentionSharingModel(mesa.Model):
    def __init__(self, number_of_vessels, width, height):
        super().__init__()

        self.number_of_vessels = number_of_vessels
        self.grid = OrthogonalMooreGrid((width, height), torus=False, random=self.random)
        self.gridgraph = GridGraph(width, height)

        print(f"\nInitializing model with {self.number_of_vessels} vessels.")

        # Create agents
        VesselAgent.create_agents(
            self,
            self.number_of_vessels,
            start_cell=[self.grid[pos] for pos in p.start_positions],
            goal_cell=[self.grid[pos] for pos in p.goal_positions],
            start_velocity=[v for v in p.start_velocities],
            tokens=[t for t in p.tokens]
        )

        # Visualize each planned path on its own property layer
        for vessel in self.agents_by_type[VesselAgent]:
            self.grid.create_property_layer(f"path_{vessel.unique_id}", default_value=0.0, dtype=float)
        self.refresh_paths_layer()

    def refresh_paths_layer(self):
        for vessel in self.agents_by_type[VesselAgent]:
            layer_name = f"path_{vessel.unique_id}"
            self.grid.set_property(layer_name, 0.0)
            for step in vessel.path:
                cell = self.grid[step[0]]
                setattr(cell, layer_name, getattr(cell, layer_name) + 1.0)
   
    def step(self):
        print(f"\n--- Time step {self.time} ---")
        # 1. Detect conflicts and negotiate if necessary
        self.agents_by_type[VesselAgent].shuffle_do("collision_avoidance")
        self.agents_by_type[VesselAgent].shuffle_do("detect_collision", radius=p.detection_radius)
        self.agents_by_type[VesselAgent].shuffle_do("move_along_path")
        
        # 2. Update paths and states
        self.refresh_paths_layer()
        self.agents_by_type[VesselAgent].shuffle_do("update_state")
        

