import pandas as pd
import os

def abortionAccess(state: str):
    """
    Returns the Abortion Access Level for a state code.
    """
    # Read the data from the CSV file
    current_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_dir, 'data', 'AbortionAccess.csv')
    df = pd.read_csv(csv_file_path)
    if state in df["state"].values:
        return df[df["state"] == state]["legal_status"].values[0]
    else:
        return "State not found."