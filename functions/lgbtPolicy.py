import pandas as pd
import os

def lgbtPolicy(state: str):
    """
    Returns the LGBT Policy Level for a state code.
    """
    current_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_dir, 'data', 'LGBTPolicy.csv')

    # Read the data from the CSV file
    df = pd.read_csv(csv_file_path)
    if state in df['State'].values:
        return df[df['State'] == state]['Level'].values[0]
    else:
        return "State not found."