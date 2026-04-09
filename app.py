from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle

from agents import VesselAgent
from model import IntentionSharingModel

import parameters as p

# Create the model instance
model_instance = IntentionSharingModel(
    number_of_vessels=p.number_of_vessels,
    width=p.width,
    height=p.height,
)

def agent_portrayal(agent):
    if isinstance(agent, VesselAgent):
        return AgentPortrayalStyle(color="tab:orange", marker="o", size=200)
    return None

def property_layer_portrayal(layer):
    if layer.name == "paths":
        return PropertyLayerStyle(color="tab:blue", alpha=0.3, colorbar=False)
    return None

model_params = {
    "number_of_vessels": p.number_of_vessels,
    "width": p.width,
    "height": p.height,
}

renderer = (
    SpaceRenderer(model=model_instance, backend="matplotlib")
    .setup_agents(agent_portrayal)
    .setup_propertylayer(property_layer_portrayal)
    .render()
)

page = SolaraViz(
    model_instance,
    renderer,
    model_params=model_params,
    name="Intention Sharing Model",
)
