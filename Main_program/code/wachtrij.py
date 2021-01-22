import json
import pandas as pd
from Main_program.code.overig_functies import csv2pd
from tqdm import tqdm
import re

df = csv2pd('BOS210_20210108_20210112.csv')

def lane_group(df):
    """
    Makes nested list with all of the sensors and corresponding traffic lights
    :param df: pandas dataframe from the intersection csv
    :return: nested list
    """
    kolommen = list(df.columns)[1:]
    rijbanen = []

    for column in kolommen:
        if len(column) == 2:
            lane = [column]
            for lane_sensor in kolommen:
                if re.search(f"(^{column}[0-9])", lane_sensor): # (^{column}[0-9][0-9])|
                    lane.append(lane_sensor)
            if len(lane) >= 3:
                rijbanen.append(lane)
    return rijbanen


def wachtrij_red(rijbanen, df):
    """
    Counts the amount of cars for each lane while traffic light is red
    :param rijbanen: nested list with the time, traffic light/lane number, lane sensors
    :param df: pandas dataframe from the intersection csv
    :return: dictionary with the times and numbering of cars
    """
    w = dict()
    for lane in rijbanen:
        lane.insert(0, "time")
        s = None
        e = None
        red = False
        begin_time = None
        w[lane[1]] = dict()
        for index in tqdm(range(1, len(df[lane[1]]))):
            if df.at[index, lane[1]] != "#" and df.at[index, lane[1]] != "Z":
                if red:
                    continue
                else:
                    begin_time = df.at[index, "time"]
                    s = index
                    red = True
            else:
                if red:
                    e = index
                    red = False
                else:
                    continue
            if s != None and e != None:
                df_lane = df.loc[s:e, [x for i,x in enumerate(lane) if i!=1 or i!=3 or i!=4]]
                cars = tel_red(df_lane, s)
                w[lane[1]].update(cars)

    with open('../data/w_red.json', 'w') as fp:
        json.dump(w, fp)
    print("Done with generating w_red.json")

def tel_red(df, begin_index):
    """
    Counts amount of cars while traffic light is red for a lane
    :param df: pandas dataframe from the intersection csv
    :param begin_index: index of time when traffic light turns red
    :return: dictionary with time and numbered car
    """
    time_cars = dict()
    df_cols = df.columns.tolist()
    for lane in df:
        act = False
        cars = 0
        begin_time = None
        if lane == df_cols[2]:
            for index in range(begin_index, len(df) + begin_index):
                if df.at[index, lane] == "|":
                    if not act:
                        begin_time = df.at[index, "time"]
                        act = True
                    else:
                        continue
                else:
                    if act:
                        cars += 1
                        time_cars[begin_time] = cars
                        act = False
                    else:
                        continue
    return time_cars

wachtrij_red(lane_group(df), df)

def wachtrij_green(rijbanen, df):
    """
    Searches for timestamps where traffic lights turn green and uses tel function
    how many cars passed by while it was green/yellow
    :param rijbanen: nested list with [traffic light, sensor in front of traffic light] columns
    :param df: pandas dataframe with all of the data of an intersection
    :return: a dictionary with for each lane all of the timestamps where the light was green and how many cars passed by
    """
    wachtrijen = dict()
    for i in rijbanen:
        s = None
        e = None
        i.insert(0, "time")
        green = False
        wachtrijen[i[1]] = dict()

        for j in tqdm(range(len(df[i[1]]))): # door de index heen
            if df.loc[j, i[1]] == "#" or df.loc[j, i[1]] == "Z":
                if green:
                    continue
                else:
                    s = j
                    green = True
            else:
                if green:
                    e = j
                    green = False
                else:
                    continue
            if s != None and e != None:
                serie = df.loc[s:e, i[2]]
                cars = tel_deact(serie)
                wachtrijen[i[1]][df.at[s, i[0]]] = cars

    with open('../data/w_green.json', 'w') as fp:
        json.dump(wachtrijen, fp)
    print("Done with generating w_green.json")

def tel_deact(serie):
    """
    Counts amount of cars from a serie when there is an activation.
    When the sensor then turns off there is a car added.
    :param serie: slice from sensor column in the dataframe when the traffic light turns green
    :return: amount of cars that went by while traffic light was green
    """
    act = False
    cars = 0
    for row in serie:
        if row == "|" and act == False:
            act = True
        elif row != "|" and act == True:
            act = False
            cars += 1
    return cars

wachtrij_green(lane_group(df), df)

def wachtrij_csv(rijbanen, df):
    """
    Merges w_red and w_green into csv file, missing times are filled with interpolation
    :param rijbanen: nested list with [traffic light, sensor in front of traffic light] columns
    :param df: pandas dataframe with all of the data of an intersection
    :return: csv file with how many cars are on the lanes
    """
    tijd = df["time"]
    kolommen = [x[0] for x in rijbanen]
    df_w = pd.DataFrame(columns=kolommen)
    df_w.insert(0, "time", tijd)
    df_w = df_w.set_index('time')

    with open('../data/w_red.json') as file:
        w_red = json.load(file)
    for lane in tqdm(w_red):
        for time, car in w_red[lane].items():
            df_w.at[time, lane] = car

    with open('../data/w_green.json') as file1:
        w_green = json.load(file1)
    for lane1 in tqdm(w_green):
        for time1, car1 in w_green[lane1].items():
            df_w.at[time1, lane1] = car1

    df_w = df_w.apply(pd.to_numeric)
    df_w.interpolate(method='linear', inplace=True)
    df_w = df_w.apply(round)
    df_w = df_w.fillna(0)

    df_w.insert(0, "time", df_w.index)
    df_w.to_csv(r'C:\Users\gsvpk\PycharmProjects\Vialis-1-Verkeersimulatie'+'Wachtrij.csv',index=False)
    # if Wachtrij.csv isn't written in Vialis-1-Verkeersimulatie, the file should be placed in that folder
    
wachtrij_csv(lane_group(df), df)







