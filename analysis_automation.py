import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

# This program allows user to choose 2 corresponding files and it will join them together based on MPTC Training fulfillment (via UD). Currently supports .xlsx and .csv filetypes. The final output saved locally as master_output.csv

# a helper function to assist with status mapping
def resolve_status(statuses):
    # if unfulfilled at all, change status to unfulfilled to be safe
    if 'UNFULFILLED' in statuses.values:
        return 'UNFULFILLED'
    else:
        return 'FULFILLED'

def main():
    # file picker window, user-friendly approach to make it a *touch* easier when using python
    root = tk.Tk()
    root.withdraw()

    # prompting user input, selecting local files (currently only supports .xlsx)
    print("Please select TRAIN 1 file (.xlsx)...")
    file_1 = filedialog.askopenfilename(
        title="Select TRAIN 1 file",
        filetypes=[("Excel files", "*.xlsx")]
    )
    # prompting user input, selecting local files (currently only supports .csv)
    print("Please select TRAIN 2 file (.csv)...")
    file_2 = filedialog.askopenfilename(
        title="Select TRAIN 2 file",
        filetypes=[("CSV files", "*.csv")]
    )

    # some input validation
    if not file_1 or not file_2:
        print("Error: No files selected. Please run the script again and select both files.")
        return

    # import data using user-selected paths
    train_1 = pd.read_excel(file_1, dtype=str)
    train_2 = pd.read_csv(file_2, dtype=str)

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

    # update UDF3 Note only where a match was found, using standardized labels as seen above.
    # rows with no match are untouched
    matched = train_1['resolved_status'].notna()
    train_1.loc[matched, 'UDF3 Note'] = train_1.loc[matched, 'resolved_status'].map(status_labels)

    # drop temporary working column before export
    train_1.drop(columns=['resolved_status'], inplace=True)

    # save output to same folder as TRAIN 1 so user can find it easily
    output_dir = os.path.dirname(file_1)
    output_path = os.path.join(output_dir, 'master_output.csv')
    train_1.to_csv(output_path, index=False)
    print(f"\nScript successful - saved master_output.csv to {output_path}")

if __name__ == "__main__":
    main()