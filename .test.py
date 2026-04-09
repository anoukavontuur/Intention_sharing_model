# # Create structured agents
# VesselAgent.create_agents(
#     self,
#     self.number_of_vessels,
#     start_cell=[self.grid[pos] for pos in p.start_positions],
#     goal_cell=[self.grid[pos] for pos in p.goal_positions],
#     start_velocity=[v for v in p.start_velocities],
# )

# # Create random agents
# VesselAgent.create_agents(
#     self,
#     self.number_of_vessels,
#     start_cell=self.random.choices(self.grid.all_cells.cells, k=self.number_of_vessels),
#     goal_cell=self.random.choices(self.grid.all_cells.cells, k=self.number_of_vessels),
#     start_velocity= 1
# )