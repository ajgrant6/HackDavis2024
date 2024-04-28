import pandas as pd

def abortionAccess(state: str):
    """
    Returns the Abortion Access Level for a state code.
    """
    # Read the data from the CSV file
    df = pd.read_csv('AbortionAccess.csv')
    if state in df["state"].values:
        return df[df["state"] == state]["legal_status"].values[0]
    else:
        return "State not found."