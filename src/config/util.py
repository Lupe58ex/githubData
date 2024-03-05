import pandas as pd

def get_diff_of_dates(start_date, end_date) -> float:
    """get the difference between two dates in timestamp format"""
    start_date_in_timestamp = start_date.timestamp()
    if pd.isna(end_date):
        current_date = pd.Timestamp.now()
        end_date = pd.to_datetime(current_date)
    
    end_date_in_timestamp = end_date.timestamp()
 
    return (end_date_in_timestamp - start_date_in_timestamp)/60

