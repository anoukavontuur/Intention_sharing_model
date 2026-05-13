import pandas as pd

vessel_data_df = pd.read_csv("output/vessel_data.csv")
# print(vessel_data_df.head())

print(vessel_data_df[vessel_data_df["AgentID"] == 1]["State"])