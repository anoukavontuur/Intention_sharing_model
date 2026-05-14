import pandas as pd
import parameters as p

# KPI1
def emergency_breaks_per_collision(collisions_detected, emergency_breaks):
    if collisions_detected > 0:
        return round(emergency_breaks / collisions_detected, 2)
    return 0

# KPI2
def ratio_executed_and_original_path_cost(original_path_cost, executed_path_cost):
    if original_path_cost > 0:
        return round(executed_path_cost / original_path_cost, 2)
    return 0

def calculate_kpis(df, iteration):
    for agent_id in range(1, p.number_of_vessels + 1):

        agent_data = df[
            df["AgentID"] == agent_id
        ].sort_values("Step")

        first_row = agent_data.iloc[0]
        last_row = agent_data.iloc[-1]

        collisions_detected = last_row["Collisions detected"]
        emergency_breaks = last_row["Emergency breaks"]

        initial_cost = first_row["Path cost"]
        executed_cost = last_row["Cost so far"]

        kpi1 = emergency_breaks_per_collision(
            collisions_detected,
            emergency_breaks
        )

        kpi2 = ratio_executed_and_original_path_cost(
            initial_cost,
            executed_cost
        )

        results.append({
            "Iteration": iteration,
            "AgentID": agent_id,
            "Collisions detected": collisions_detected,
            "Emergency breaks": emergency_breaks,
            "KPI1": kpi1,
            "Initial cost": initial_cost,
            "Executed cost": executed_cost,
            "KPI2": kpi2
        })

results = []

for iteration in range(p.n_runs):
    vessel_data_df = pd.read_csv(f"output/model_output/scenario_{p.scenario}/vessel_data_run_{iteration}_{p.scenario}.csv")
    calculate_kpis(vessel_data_df, iteration)

kpi_results_df = pd.DataFrame(results)
kpi_results_df.to_csv(f"output/kpi_results/kpi_results_{p.scenario}.csv", index=False)
print(f"KPI results saved to output/kpi_results/kpi_results_{p.scenario}.csv")

summary_df = (
    kpi_results_df.groupby("AgentID")[["KPI1", "KPI2"]]
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={"KPI1": "Average KPI1", "KPI2": "Average KPI2"})
)

summary_df.to_csv(f"output/kpi_results/kpi_summary_{p.scenario}.csv", index=False)