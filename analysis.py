import pandas as pd

vessel_data_df = pd.read_csv("output/vessel_data.csv")


vessel_1_data = vessel_data_df[vessel_data_df["AgentID"] == 1]
vessel_1_data.to_csv("output/vessel1_data.csv", index=True)

