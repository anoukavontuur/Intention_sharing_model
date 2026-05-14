from model import IntentionSharingModel
import parameters as p

def run_model(n=1):
    for iteration in range(n):
        model = IntentionSharingModel(p.width, p.height)
        while model.running and model.time < p.horizon:
            model.step()

        Vesseldata = model.datacollector.get_agent_vars_dataframe()
        path = f"output/model_output/scenario_{p.scenario}/vessel_data_run_{iteration}_{p.scenario}.csv"
        Vesseldata.to_csv(path, index=True)

run_model(n=p.n_runs)
