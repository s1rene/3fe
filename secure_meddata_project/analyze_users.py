import pandas as pd

df = pd.read_csv("results/user_simulation_log.csv")
stats = df.groupby("role")["duration_s"].agg(["count", "mean", "std", "min", "max"]).round(3)
print(stats)
