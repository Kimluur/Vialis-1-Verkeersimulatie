"""
Zet alle tijden om naar datetime datatype.
Voegt 1 uur toe aan alle tijden.
"""

import pandas as pd
from datetime import timedelta


def add_hour(datafr):
    datafr.timestamp = pd.DatetimeIndex(datafr.timestamp) + timedelta(hours=1)


def main():
    df = pd.read_csv('1.csv', delimiter=";")

    df.timestamp = df.timestamp.str.slice(stop=19)

    add_hour(df)

    print(df)


if __name__ == '__main__':
    main()
