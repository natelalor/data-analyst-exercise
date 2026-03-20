import pandas as pd

# This script reads TRAIN_1 and TRAIN_2, resolves the requirement completion status for each user, and updates TRAIN_1's UDF3 Note accordingly. The final output is saved as master_output.csv.
def main():

    # import data
    train_1 = pd.read_excel("datasets/TRAIN_1.xlsx", dtype=str)
    train_2 = pd.read_csv("datasets/TRAIN_2.csv", dtype=str)

    # initial cleaning & standardization - preparing join
    train_1["MPTC User ID"] = train_1["MPTC User ID"].str.strip()
    train_2["User ID"] = train_2["User ID"].str.strip()
    train_2['Requirement Completion Status'] = train_2['Requirement Completion Status'].str.strip()
    train_2['Requirement Completion Status'] = train_2['Requirement Completion Status'].str.upper()
        
    # grouping by User ID & Completion Status, as well as fulfillment qualifier before we join
    user_id_to_status_map = train_2.groupby('User ID')['Requirement Completion Status'].apply(resolve_status)

    # temporary column to match train_1 status with train_2 through pandas mapping
    # returns NaN if unsufficient status
    train_1['resolved_status'] = train_1['MPTC User ID'].map(user_id_to_status_map)

    # if user id is found in train 1, update status FULFILLED or UNFULFILLED
    # matched is a column representing sufficient status for train_1 IDs
    matched = train_1['resolved_status'].notna()

    # then locates instances where matched = true, then update to new status via train_2
    train_1.loc[matched, 'UDF3 Note'] = train_1.loc[matched, 'resolved_status']

    # cleanup
    train_1.drop(columns=['resolved_status'], inplace=True)

    # save into separate file that is sucessfully both train_1 joined with viable train_2 content
    train_1.to_csv('/datasets/master_output.csv', index=False)
    print("\nScript successful - saved master_output.csv")

# completion status signifier - helper function primarily for train_2 with additional cleaning - missing FULFILLED keyword will produce unfulfillment for further manual inquiry
def resolve_status(statuses):
    if 'FULFILLED' in statuses.values:
        return 'FULFILLED'
    else:
        return 'UNFULFILLED'