"""
Zet alle tijden om naar datetime datatype.
Voegt 1 uur toe aan alle tijden.
"""

import pandas as pd
from datetime import timedelta


def add_hour(datafr):
    datafr.timestamp = pd.DatetimeIndex(datafr.timestamp) + timedelta(hours=1)


def get_routes(datafr):
    routes = [[117, 193],
              [282, 294],
              [462, 476],
              [1010, 1026],
              [1101, 1115]]

    route_1 = pd.DataFrame(datafr[['timestamp', 'latitude', 'longitude', 'speed']][117:193])
    route_2 = pd.DataFrame(datafr[['timestamp', 'latitude', 'longitude', 'speed']][282:295])
    route_3 = pd.DataFrame(datafr[['timestamp', 'latitude', 'longitude', 'speed']][462:477])
    route_4 = pd.DataFrame(datafr[['timestamp', 'latitude', 'longitude', 'speed']][1010:1027])
    route_5 = pd.DataFrame(datafr[['timestamp', 'latitude', 'longitude', 'speed']][1101:1116])

    dataframes = route_1.append(route_2.append(route_3.append(route_4.append(route_5))))

    return dataframes


def main():
    df = pd.read_csv('1.csv', delimiter=";")

    df.timestamp = df.timestamp.str.slice(stop=19)

    add_hour(df)

    dfRoute = get_routes(df)
    dfRoute.to_csv('routes.csv')


if __name__ == '__main__':
    main()
