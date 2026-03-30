from mesa.discrete_space import CellAgent

class VesselAgent(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell

    def say_hi(self):
        print(f"Hi, I'm agent {self.unique_id} on cell {self.cell.coordinate}!")