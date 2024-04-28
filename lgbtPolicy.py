import pandas as pd

def lgbtPolicy(state: str):
    """
    Returns the LGBT Policy Level for a state code.
    """
    # Read the data from the CSV file
    df = pd.read_csv('LGBTPolicy.csv')
    if state in df['State'].values:
        return df[df['State'] == state]['Level'].values[0]
    else:
        return "State not found."