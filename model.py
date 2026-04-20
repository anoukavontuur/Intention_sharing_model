from agents import VesselAgent
from pathfinding import GridGraph
import parameters as p

import mesa
from mesa.discrete_space import OrthogonalMooreGrid

class IntentionSharingModel(mesa.Model):
    def __init__(self, number_of_vessels, width, height):
        super().__init__()

        self.number_of_vessels = number_of_vessels
        self.grid = OrthogonalMooreGrid((width, height), torus=False, random=self.random)
        self.gridgraph = GridGraph(width, height)

        # Create agents
        VesselAgent.create_agents(
            self,
            self.number_of_vessels,
            start_cell=[self.grid[pos] for pos in p.start_positions],
            goal_cell=[self.grid[pos] for pos in p.goal_positions],
            start_velocity=[v for v in p.start_velocities],
        )

        # Initial path planning for all agents
        self.agents_by_type[VesselAgent].do("set_pathspace", graph=self.gridgraph)
        self.agents_by_type[VesselAgent].do("set_path")

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
        for vessel in self.agents_by_type[VesselAgent]:
            if vessel.detect_collision(radius=p.detection_radius):
                for collision_vessel in vessel.collision_agents:
                    vessel.generate_alternative_path(graph=self.gridgraph, reservation_table=collision_vessel.path)

        self.agents_by_type[VesselAgent].do("move_along_path")
        self.refresh_paths_layer()

