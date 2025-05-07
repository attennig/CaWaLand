
import pandas as pd

traces_path = "./data_preprocessing/traces/spark/traces.csv"
traces_df = pd.read_csv(traces_path)
traces_df.drop(columns=["platform", "CPU_freq", "n_vCPU","mem_size_GB", "avg_kbmemused", "avg_%memused", "avg_%usr"], inplace=True)
# There are some negative runtimes in the scout dataset
traces_df = traces_df[traces_df["runtime_sec"] >= 0]

traces_df = traces_df[traces_df["algorithm"].isin(["sort", "join"])]
from sklearn.linear_model import LinearRegression
import numpy as np

out_py = "expected_runtime = {\n"
# Iterate through each algorithm
for algorithm, group_df in traces_df.groupby(["algorithm", "VM_instance"]):
    # Prepare the data for regression
    X = group_df[["n_nodes", "input_size_bytes"]].values
    y = group_df["runtime_sec"].values

    # Fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    out_py += f"    {algorithm} : lambda n_nodes, input_size_bytes: {model.coef_[0]}*n_nodes + {model.coef_[1]} * input_size_bytes + {model.intercept_},\n"

out_py = out_py[:-2] + "\n}\n"



with open("./models/expected_runtime.py", "w") as f:
    f.write(out_py)