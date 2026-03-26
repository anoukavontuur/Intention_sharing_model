from mesa.experimental.continuous_space import ContinuousSpace, ContinuousSpaceAgent

class VesselAgent(ContinuousSpaceAgent):
    """An agent representing a vessel with a speed and position"""

    def __init__(self, space, model, speed=1.0):
        super().__init__(space, model)

        # Variables
        self.speed = speed

    @classmethod    
    def create_agents(cls, model, space, n):
        """Create n agents, add them to the model and return a list"""
        agents = []
        for _ in range(n):
            agent = cls(space, model)
            # Random position within space bounds
            x = model.random.uniform(space.x_min, space.x_max)
            y = model.random.uniform(space.y_min, space.y_max)
            pos = (x, y)
            agent.pos = pos
            space.agents.add(agent)
            agents.append(agent)
            print (f"Agent created at position {pos}")
        return agents
    
