from mesa.visualization import SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle
from matplotlib.path import Path as MplPath
from matplotlib import transforms
import math

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
        # Create a small triangular arrow Path pointing up, then rotate to match heading vector.
        heading = getattr(agent, "heading", 1)

        # Heading vectors (match pathfinding.all_directions)
        all_directions = [
            (-1, 1), (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1), (-1, 0)
        ]

        dx, dy = all_directions[heading % len(all_directions)]
        # Compute angle of the heading vector in degrees
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # Our base triangle points up (0,1). Rotate so its tip aligns with heading vector.
        # Matplotlib 0deg is along +x; base up corresponds to 90deg, so rotation = angle_deg - 90
        rot_deg = angle_deg - 90

        # Base equilateral triangle pointing up, centered at origin with constant radius
        r = 0.45
        # angles for top, bottom-left, bottom-right (degrees)
        angles_deg = [90, 210, 330]
        verts = []
        for a in angles_deg:
            rad = math.radians(a)
            verts.append((r * math.cos(rad), r * math.sin(rad)))
        verts.append(verts[0])

        # Apply rotation
        rot = transforms.Affine2D().rotate_deg(rot_deg)
        rotated = rot.transform(verts)

        mpl_path = MplPath(rotated)
        return AgentPortrayalStyle(color=_agent_color(agent), marker=mpl_path, size=200)
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
