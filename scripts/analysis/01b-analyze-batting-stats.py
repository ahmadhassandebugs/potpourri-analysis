## run 01a before this script

from os import path
import pandas as pd

from utils.context import data_processed_dir

### Config ###
DATA_FOLDER = PROCESSED_DATA_FOLDER = path.join(data_processed_dir, "batting-stats")
filter_runs_dict = {"test": 1500, "odi": 1000, "t20": 500}  # filter new players

# load batting stats and filter players based on runs
test_df = pd.read_csv(path.join(DATA_FOLDER, "test.csv"))
test_df = test_df[test_df["runs"] >= filter_runs_dict["test"]]
odi_df = pd.read_csv(path.join(DATA_FOLDER, "odi.csv"))
odi_df = odi_df[odi_df["runs"] >= filter_runs_dict["odi"]]
t20_df = pd.read_csv(path.join(DATA_FOLDER, "t20.csv"))
t20_df = t20_df[t20_df["runs"] >= filter_runs_dict["t20"]]
t20_df.rename(columns={"average": "average_t20", "strikerate": "strikerate_t20", "runs": "runs_t20"}, inplace=True)

# merge data across formats
temp_df = test_df.merge(odi_df, on="player", how="inner", suffixes=("_test", "_odi"))
merged_df = temp_df.merge(t20_df, on="player", how="inner")
del temp_df

# save the file
merged_df.to_csv(path.join(PROCESSED_DATA_FOLDER, "combined.csv"), index=False, header=True)

print("Complete../")
