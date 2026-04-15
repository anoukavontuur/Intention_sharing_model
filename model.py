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
        self.agents_by_type[VesselAgent].do("set_path", graph=self.gridgraph)

        # Visualize planned paths on a property layer
        self.grid.create_property_layer("paths", default_value=0.0, dtype=float)
        self.refresh_paths_layer()

    def refresh_paths_layer(self):
        self.grid.set_property("paths", 0.0)
        for vessel in self.agents_by_type[VesselAgent]:
            for coordinate in vessel.plan.values():  # plan is a dict {t: (x, y)}
                self.grid[coordinate].paths += 1.0
   
    def step(self):
        self.agents_by_type[VesselAgent].do("detect_collision", radius=4)
        for a in self.agents_by_type[VesselAgent]:
            print(f"collision agents for agent {a.unique_id}: {a.collision_agents}")

        self.agents_by_type[VesselAgent].do("move_along_path")
        self.refresh_paths_layer()
