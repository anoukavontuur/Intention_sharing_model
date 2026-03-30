from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

from model import IntentionSharingModel

IntentionSharingModel = IntentionSharingModel(number_of_vessels=2, width=10, height=10)

def agent_portrayal(agent):
    return AgentPortrayalStyle(color="tab:orange", size=50)

model_params = {
    "number_of_vessels": 2,
    "width": 10,
    "height": 10,
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

