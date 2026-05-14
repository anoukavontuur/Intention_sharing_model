from model import IntentionSharingModel
from agents import VesselAgent
from conflict_detection import has_conflict
import parameters as p

model = IntentionSharingModel(p.width, p.height)
while model.running and model.time < p.horizon:
    model.step()

Vesseldata = model.datacollector.get_agent_vars_dataframe()
Vesseldata.to_csv("output/vessel_data.csv", index=True)
