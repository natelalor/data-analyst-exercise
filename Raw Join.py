import pandas as pd

# This script reads TRAIN_1 and TRAIN_2, resolves the requirement completion
# status for each user, and updates TRAIN_1's UDF3 Note accordingly.
# The final output is saved as master_output.csv.

# a helper function to assist with status mapping
def resolve_status(statuses):
    # if unfulfilled at all, change status to unfulfilled to be safe
    if 'UNFULFILLED' in statuses.values:
        return 'UNFULFILLED'
    else:
        return 'FULFILLED'

def main():
    # import data
    train_1 = pd.read_excel("datasets/TRAIN 1.xlsx", dtype=str)
    train_2 = pd.read_csv("datasets/TRAIN 2.csv", dtype=str)

    # initial cleaning & standardization - preparing join
    train_1["MPTC User ID"] = train_1["MPTC User ID"].str.strip()
    train_2["User ID"] = train_2["User ID"].str.strip()
    train_2['Requirement Completion Status'] = train_2['Requirement Completion Status'].str.strip().str.upper()

    # collapse train_2 to one row per user with conservative conflict resolution
    user_id_to_status_map = train_2.groupby('User ID')['Requirement Completion Status'].apply(resolve_status)

    # map resolved statuses onto train_1 - NaN where no match found
    train_1['resolved_status'] = train_1['MPTC User ID'].map(user_id_to_status_map)

    # map raw FULFILLED/UNFULFILLED to TRAIN 1 standard descriptive format
    status_labels = {
        'FULFILLED':   'Training Year (TY) 25 In-Service Fulfilled',
        'UNFULFILLED': 'Training Year (TY) 25 In-Service UnFulfilled'
    }

    # update UDF3 Note only where a match was found, using standardized labels as seen above
    # rows with no match are untouched
    matched = train_1['resolved_status'].notna()
    train_1.loc[matched, 'UDF3 Note'] = train_1.loc[matched, 'resolved_status'].map(status_labels)

    # drop temporary working column before export
    train_1.drop(columns=['resolved_status'], inplace=True)

    # save final output
    train_1.to_csv('datasets/master_output.csv', index=False)
    print("\nScript successful - saved master_output.csv")

if __name__ == "__main__":
    main()