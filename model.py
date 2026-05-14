from agents import VesselAgent
from pathfinding import GridGraph, path_cost, visualization_path
import parameters as p

import mesa
from mesa.discrete_space import OrthogonalMooreGrid

class IntentionSharingModel(mesa.Model):
    def __init__(self, width, height):
        super().__init__()

        self.number_of_vessels = len(p.agents)
        self.grid = OrthogonalMooreGrid((width, height), torus=False, random=self.random)
        self.gridgraph = GridGraph(width, height)

        # Initiating data collector
        self.datacollector = mesa.DataCollector(
            agent_reporters={"State": "state",
                             "Cost so far": lambda a: path_cost(a.travelled_path),
                             "Collisions detected": "collisions_detected",
                             "Emergency breaks": "emergency_breaks"
                             }
        )

        print(f"\nInitializing model with {self.number_of_vessels} vessels.")

        for agent in p.agents:
            VesselAgent.create_agents(
                self,
                1,
                start_cell = self.grid[agent[0]],
                goal_cell = self.grid[agent[1]],
                start_heading = agent[2],
                start_velocity = agent[3],
                tokens = agent[4]
            )

        # Visualize each planned path on its own property layer
        for vessel in self.agents_by_type[VesselAgent]:
            self.grid.create_property_layer(f"path_{vessel.unique_id}", default_value=0.0, dtype=float)
        self.refresh_paths_layer()

        self.datacollector.collect(self)

    def refresh_paths_layer(self):
        for vessel in self.agents_by_type[VesselAgent]:
            layer_name = f"path_{vessel.unique_id}"
            self.grid.set_property(layer_name, 0.0)
            for step in visualization_path(vessel.path):
                cell = self.grid[step[0]]
                setattr(cell, layer_name, getattr(cell, layer_name) + 1.0)
   
    def step(self):
        print(f"\n--- Time step {self.time} ---")

        # 1. Detect conflicts and negotiate if necessary
        print("\nCollision avoidance phase:")
        self.agents_by_type[VesselAgent].shuffle_do("collision_avoidance")

        print("\nMovement phase:")
        self.agents_by_type[VesselAgent].shuffle_do("move_along_path")
        
        # 2. Update paths and states
        self.refresh_paths_layer()
        self.agents_by_type[VesselAgent].shuffle_do("update_state")
        self.datacollector.collect(self)

        # 3. Check if all vessels have reached their goals
        if all(vessel.cell.coordinate == vessel.goal.coordinate for vessel in self.agents_by_type[VesselAgent]):
            print("\nAll vessels have reached their goals. Stopping the model.")
            self.running = False
        
