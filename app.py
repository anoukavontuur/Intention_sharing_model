from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle

from agents import MarkerAgent, VesselAgent
from model import IntentionSharingModel

import parameters as p

IntentionSharingModel = IntentionSharingModel(number_of_vessels=p.number_of_vessels, width=p.width, height=p.height, start_coordinate=p.start_coordinate, goal_coordinate=p.goal_coordinate)

def agent_portrayal(agent):
    if isinstance(agent, VesselAgent):
        portrayal = AgentPortrayalStyle(color="tab:orange", marker="^", size=50)
    elif isinstance(agent, MarkerAgent):
        portrayal = AgentPortrayalStyle(color="tab:red", marker="x", size=30)
    return portrayal

model_params = {
    "number_of_vessels": p.number_of_vessels,
    "width": p.width,
    "height": p.height,
    "start_coordinate": p.start_coordinate,
    "goal_coordinate": p.goal_coordinate
}

renderer = (
    SpaceRenderer(model=IntentionSharingModel, backend="matplotlib")
    .setup_agents(agent_portrayal)
    .render()
)

page = SolaraViz(
    IntentionSharingModel,
    renderer,
    model_params=model_params,
    name = "Intention Sharing Model"
)

