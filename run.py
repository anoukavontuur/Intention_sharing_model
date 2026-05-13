from model import IntentionSharingModel
from agents import VesselAgent
from conflict_detection import has_conflict
import parameters as p

model = IntentionSharingModel(p.width, p.height)
while model.running and model.time < p.horizon:
    model.step()

Vesseldata = model.datacollector.get_agent_vars_dataframe()

Vesseldata.to_csv("output/vessel_data.csv", index=True)

print("\nConflict analysis:")
for vessel1 in model.agents_by_type[VesselAgent]:
    for vessel2 in model.agents_by_type[VesselAgent]:
        if vessel1.unique_id != vessel2.unique_id:
            path1 = vessel1.taken_path
            path2 = vessel2.taken_path
            if has_conflict(path1, path2):
                print(f"Conflict detected between Vessel {vessel1.unique_id} and Vessel {vessel2.unique_id}")
                print(f"Vessel {vessel1.unique_id} path: {path1}")
                print(f"Vessel {vessel2.unique_id} path: {path2}")
print("Done with conflict analysis.")