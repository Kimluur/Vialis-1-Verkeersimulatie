"""
Zet alle tijden om naar datetime datatype.
Voegt 1 uur toe aan alle tijden.
"""

import pandas as pd
from datetime import timedelta


def add_hour(datafr):
    datafr.timestamp = pd.DatetimeIndex(datafr.timestamp) + timedelta(hours=1)


def main():
    # Lees CSV
    df = pd.read_csv('1.csv', delimiter=";")

    # Converteer 'timestamp' om naar datetime
    df.timestamp = df.timestamp.str.slice(stop=19)

    # Voeg één uur toe aan tijd, als correctie
    add_hour(df)

    # Vul tijden in met milliseconden
    df = df.set_index('timestamp').resample("100ms").first().reset_index().reindex(columns=df.columns)
    cols = df.columns.difference(
        ['latitude', 'longitude'])
    df[cols] = df[cols].ffill()

    # Zet tijd in juiste format
    df['timestamp'] = df["timestamp"].dt.strftime("%m-%d-%Y %H:%M:%S.%f")

    print(df)


if __name__ == '__main__':
    main()
