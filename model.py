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
        self.GridGraph = GridGraph(width, height)

        # Create (structured) agents
        VesselAgent.create_agents(
            self,
            self.number_of_vessels,
            start_cell=[self.grid[pos] for pos in p.start_positions],
            goal_cell=[self.grid[pos] for pos in p.goal_positions],
            start_velocity=[v for v in p.start_velocities],
        )

        # # Create random paths for the agents
        # VesselAgent.create_agents(
        #     self,
        #     self.number_of_vessels,
        #     start_cell=self.random.choices(self.grid.all_cells.cells, k=self.number_of_vessels),
        #     goal_cell=self.random.choices(self.grid.all_cells.cells, k=self.number_of_vessels),
        #     start_velocity= 1
        # )

        self.agents_by_type[VesselAgent].do("set_path")
        self.grid.create_property_layer("paths", default_value=0.0, dtype=float)
        self.refresh_paths_layer()

        self.agents_by_type[VesselAgent].do("planning_horizon")
        self.agents_by_type[VesselAgent].do("detect_nearby_vessels", radius=p.detection_radius)

    def refresh_paths_layer(self):
        self.grid.set_property("paths", 0.0)
        for vessel in self.agents_by_type[VesselAgent]:
            for coordinate in vessel.path:
                self.grid[coordinate].paths += 1.0
   
    def step(self):
        self.agents_by_type[VesselAgent].do("planning_horizon")
        self.agents_by_type[VesselAgent].do("detect_nearby_vessels", radius=p.detection_radius)
        self.agents_by_type[VesselAgent].do("move_along_path")
        self.refresh_paths_layer()


