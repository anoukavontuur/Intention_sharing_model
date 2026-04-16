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

        # Visualize planned paths on a property layer
        self.grid.create_property_layer("paths", default_value=0.0, dtype=float)
        self.refresh_paths_layer()
        

    def refresh_paths_layer(self):
        self.grid.set_property("paths", 0.0)
        for vessel in self.agents_by_type[VesselAgent]:
            for step in vessel.path:
                self.grid[step[0]].paths += 1.0
   
    def step(self):
        for agent in self.agents_by_type[VesselAgent]:
            if agent.detect_collision(radius=4):
                print("Collision detected! Agents will replan their paths.")
                for collision_agent in agent.collision_agents:
                    agent.generate_alternative_path(graph=self.gridgraph, reservation_table=collision_agent.path)

        self.agents_by_type[VesselAgent].do("move_along_path")
        self.refresh_paths_layer()

