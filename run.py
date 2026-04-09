from model import IntentionSharingModel
import parameters as p

model = IntentionSharingModel(
    number_of_vessels=p.number_of_vessels,
    width=p.width,
    height=p.height,
    planning_horizon=p.planning_horizon
)
model.step()