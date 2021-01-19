"""
Zet alle tijden om naar datetime datatype.
Voegt 1 uur toe aan alle tijden.
"""

import pandas as pd
from datetime import timedelta



def add_hour(datafr):
    """
    Voegt een uur toe aan 'timestamp', omdat de tijd verkeerd was.

    :return DataFrame
    """
    datafr.timestamp = pd.DatetimeIndex(datafr.timestamp) + timedelta(hours=1)

    return datafr


def fill_coords(datafr):
    """
    Interpoleert op cellen met NaN waarden

    :return DataFrame
    """
    # df_dropped_na = datafr.dropna()
    # nonNA = list(df_dropped_na.index.values)
    #
    # for i in range(len(nonNA) - 1):
    #     prev_lat = datafr.at[nonNA[i], 'latitude']
    #     diff_lat = abs(datafr.at[nonNA[i], 'latitude'] - datafr.at[nonNA[i + 1], 'latitude'])
    #     diff_lat /= (nonNA[i + 1] - 2)
    #
    #     for j in range((nonNA[i + 1] - nonNA[i]) - 1):
    #         prev_lat += diff_lat
    #         datafr.at[nonNA[j + 1], 'latitude'] = prev_lat
    #         print(datafr.at[nonNA[j + 1], 'latitude'])

    # Er is een interpolatie functie in Pandas >->
    datafr.interpolate(method='quadratic', inplace=True)

    return datafr


def fix_timestamp(datafr):
    """
    Timestamps hebben onnodig veel nullen aan het einde.
    Deze functie haalt die onnodige nullen weg

    :return DataFrame
    """

    datafr['timestamp'] = datafr['timestamp'].str.slice(stop=21)

    return datafr


def main():
    # Lees CSV
    df = pd.read_csv('1.csv', delimiter=";")

    # Converteer 'timestamp' om naar datetime
    df.timestamp = df.timestamp.str.slice(stop=19)

    # Voeg één uur toe aan tijd, als correctie
    df = add_hour(df)

    # Vul tijden in met milliseconden
    df = df.set_index('timestamp').resample("100ms").first().reset_index().reindex(columns=df.columns)
    cols = df.columns.difference(
        ['latitude', 'longitude', 'speed'])
    df[cols] = df[cols].ffill()

    # Zet tijd in juiste format
    df['timestamp'] = df["timestamp"].dt.strftime("%d-%m-%Y %H:%M:%S.%f")

    # Interpoleer op cellen met NaN waarden
    df = fill_coords(df)

    # Fix de timestamps
    df = fix_timestamp(df)

    print(df)


if __name__ == '__main__':
    main()
