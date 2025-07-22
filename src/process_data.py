import pandas as pd

def process_data(df):
    # Ensure datetime
    df['time'] = pd.to_datetime(df['time'])

    # Fill missing values (forward then backward)
    df = df.fillna(method='ffill').fillna(method='bfill')

    # Feature engineering
    df['temperature_avg'] = (df['temperature_2m_max'] + df['temperature_2m_min']) / 2
    df['temperature_range'] = df['temperature_2m_max'] - df['temperature_2m_min']
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month

    return df
