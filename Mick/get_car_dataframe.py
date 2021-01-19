import pandas as pd
from datetime import timedelta

def add_hour(datafr):
    datafr.timestamp = pd.DatetimeIndex(datafr.timestamp) + timedelta(hours=1)

def fill_coords(datafr):
    datafr.interpolate(method='quadratic', inplace=True)

    return datafr

def fix_timestamp(datafr):
    datafr['timestamp'] = datafr['timestamp'].str.slice(stop=21)

def main_dataframe():
    # Lees CSV
    df = pd.read_csv('1.csv', delimiter=";")

    # Converteer 'timestamp' om naar datetime
    df.timestamp = df.timestamp.str.slice(stop=19)

    # Voeg één uur toe aan tijd, als correctie
    add_hour(df)

    # Vul tijden in met milliseconden
    df = df.set_index('timestamp').resample("100ms").first().reset_index().reindex(columns=df.columns)
    cols = df.columns.difference(
        ['latitude', 'longitude', 'speed'])
    df[cols] = df[cols].ffill()

    # Zet tijd in juiste format
    df['timestamp'] = df["timestamp"].dt.strftime("%d-%m-%Y %H:%M:%S.%f")

    df = fill_coords(df)

    fix_timestamp(df)

    return df