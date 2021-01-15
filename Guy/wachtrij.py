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

def wachtrij_achteraf(rijbanen, df):
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
    return wachtrijen


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

# print(wachtrij_achteraf(rijbanen, df))
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

# wachtrij()







