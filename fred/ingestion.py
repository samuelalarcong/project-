import pandas as pd
from fredapi import Fred

def fetch_series(series_id, api_key, start_date=None, end_date=None, frequency=None, reset_index=True):
    """
    Fetch a FRED series and return as a DataFrame.
    """
    fred = Fred(api_key=api_key)
    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    
    df = pd.DataFrame(data, columns=[series_id])
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    
    # Resample if frequency is specified
    if frequency:
        df = df.resample(frequency).last()
    
    if reset_index:
        df = df.reset_index()
    
    return df
