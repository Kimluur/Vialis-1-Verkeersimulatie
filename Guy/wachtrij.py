import json
import pandas as pd
import numpy as np
from Guy.Vialis_Functies import csv2pd
from tqdm import tqdm


df = csv2pd('BOS210.csv')
rijbanen = [['01','011'],
                ['03', '031'],
                ['04', '041'],
                ['05', '051'],
                ['11', '111'],
                ['12', '121'],
                ['41', '411']]
rijbanen_full = [['01','011', '014'],
                ['03','031', '034'],
                ['04','041', '044'],
                ['05','051', '054'],
                ['11','111', '114'],
                ['12','121', '124'],
                ['41','411', '412']]


def wachtrij(rijbanen):
    """
    Counts how many cars went by in a day for every lane
    :param rijbanen: a list with all possible lanes
    :return:
    """
    rijbanen = ['011','031','041','051','111','121','411']
    # df = csv2pd('BOS210.csv')

    for i in rijbanen:
        print(f"{i[0]}: " + tel(df[i]))
        return

def tel(df1):
    """
    Counts how many times a sensor turns on.
    :param df1: pandas serie
    :return: the amount of cars as string
    """
    cars = 0
    is_act = False
    for row in df1:
        if row == "|":
            if is_act:
                pass
            else:
                cars += 1
                is_act = True
        else:
            if is_act:
                is_act = False
    return str(cars)


def wachtrij_red(rijbanen_full, df):
    """

    :param rijbanen_full: nested list with the columns [time, lane traffic light, 1st sensor, 4th sensor]
    :param df: pandas dataframe from the intersection csv
    :return: dictionary with the times and numbering of cars
    """
    w = dict()
    for lane in rijbanen_full:
        lane.insert(0, "time")
        s = None
        e = None
        red = False
        begin_time = None
        w[lane[2]] = dict()
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
                df_lane = df.loc[s:e, [x for i,x in enumerate(lane) if i!=1]]
                cars = tel_red(df_lane, s)
                w[lane[2]].update(cars)

    with open('w_red.json', 'w') as fp:
        json.dump(w, fp)

def tel_red(df, begin_index):
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

# wachtrij_red(rijbanen_full, df)


def wachtrij_green(rijbanen, df):
    """
    Searches for timestamps where traffic lights turn green and uses tel function
    how many cars passed by while it was green/yellow
    :param rijbanen: nested list with [traffic light, sensor in front of traffic light] columns
    :param df: pandas dataframe with all of the data of an intersection
    :return: a dictionary with for each lane all of the timestamps where the light was green and how many cars passed by
    """
    wachtrijen = dict()
    for i in tqdm(rijbanen):
        s = None
        e = None
        i.insert(0, "time")
        green = False
        wachtrijen[i[2]] = dict()

        for j in range(len(df[i[1]])): # door de index heen
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
                wachtrijen[i[2]][df.at[s, i[0]]] = cars

    with open('w_green.json', 'w') as fp:
        json.dump(wachtrijen, fp)

def tel_deact(serie):
    """
    Counts amount of cars from a serie when there is an activation.
    When the sensor then turns off there is a car added.
    :param serie:
    :return:
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

# wachtrij_green(rijbanen, df)


def wachtrij_df(df):
    tijd = df["time"]
    kolommen = ['011', '031', '041', '051', '111', '121', '411']
    df_w = pd.DataFrame(columns=kolommen)
    df_w.insert(0, "time", tijd)
    df_w = df_w.set_index('time')

    with open('w_red.json') as file:
        w_red = json.load(file)
    for lane in tqdm(w_red):
        for time, car in w_red[lane].items():
            # index = df[df["time"] == time].index.values[0]
            df_w.at[time, lane] = car

    with open('w_green.json') as file1:
        w_green = json.load(file1)
    for lane1 in tqdm(w_green):
        for time1, car1 in w_green[lane1].items():
            # index1 = df[df["time"] == time1].index.values[0]
            df_w.at[time1, lane1] = car1

    df_w = df_w.apply(pd.to_numeric)
    df_w.interpolate(method='linear', inplace=True)
    df_w = df_w.apply(round)

    # TODO: zodra laatste keer groen is zou je het aantal auto's naar 0 kunnen laten gaan. Dus voeg bij laatste tijdstip dat het groen/geel een 0 waarde in zodat er een vloeiendere loop is tussen groen en rood waardes.
    return df_w

wachtrij_df(df)







