import pandas as pd

# This script reads TRAIN_1 and TRAIN_2, resolves the requirement completion status for each user, and updates TRAIN_1's UDF3 Note accordingly. The final output is saved as master_output.csv.

# import data
train_1_raw = pd.read_excel("/mnt/user-data/uploads/TRAIN_1.xlsx", dtype=str)
train_2_raw = pd.read_csv("/mnt/user-data/uploads/TRAIN_2.csv", dtype=str)

# initial cleaning & standardization
train_1_raw["MPTC User ID"] = train_1_raw["MPTC User ID"].str.strip()
train_2_raw["User ID"] = train_2_raw["User ID"].str.strip()
