from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle

from agents import VesselAgent
from model import IntentionSharingModel

import parameters as p

AGENT_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


def _agent_color(agent):
    return AGENT_COLORS[(agent.unique_id - 1) % len(AGENT_COLORS)]


def _agent_color_by_id(unique_id):
    return AGENT_COLORS[(unique_id - 1) % len(AGENT_COLORS)]

# Create the model instance
model_instance = IntentionSharingModel(
    number_of_vessels=p.number_of_vessels,
    width=p.width,
    height=p.height,
)

def agent_portrayal(agent):
    if isinstance(agent, VesselAgent):
        return AgentPortrayalStyle(color=_agent_color(agent), marker="o", size=200)
    return None

def property_layer_portrayal(layer):
    if layer.name.startswith("path_"):
        vessel_id = int(layer.name.split("_", 1)[1])
        return PropertyLayerStyle(color=_agent_color_by_id(vessel_id), alpha=0.25, colorbar=False)
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
