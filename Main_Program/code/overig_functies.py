import csv
import datetime
import json

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

rijbanen = [['01','011'],
                ['03', '031'],
                ['04', '041'],
                ['05', '051'],
                ['11', '111'],
                ['12', '121'],
                ['41', '411']]

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

def give_index(column_name):
    """
    Gives back index of column name in the header
    :param column_name: string with column name from csv file BOS210.csv
    :return: index (integer)
    """
    header = ['time', '01', '03', '04', '05', '11', '12', '22', '24', '28', '31', '32', '37', '38', '41', '011', '012', '013', '014', '031', '032', '033', '034', '041', '042', '043', '044', '051', '052', '053', '054', '111', '112', '113', '114', '121', '122', '123', '124', '221', '222', '223', 'K22', '241', 'K24', '281', 'K28', 'K311', 'K312321', 'K322', 'K371', 'K372381', 'K382', '411', '412', 'F055']
    print(header.index(column_name))

def velocity():
    """
    Reads csv to see how long an activation is and with the distance that
    calculates the velocity in km/h
    :return: velocity in km/h
    """
    sensor = []
    activation = False
    with open('../../BOS210.csv') as f:
        r = csv.reader(f, delimiter=';')
        for i in r:
            if i[17] == '|' and activation == False:
                sensor.append(i[17])
                activation = True
            elif i[17] == '|' and activation == True:
                sensor.append(i[17])
            elif i[17] == '' and activation == True:
                activation = False
                break
    dur_act = len(sensor) / 10
    len_sensor = 18
    return (18 / dur_act) * 3.6


def busy_graph():
    """
    Creates graph that points out what times are busy on the intersection
    :return: Matplotlib graph
    """
    with open('../../BOS210.csv') as f:
        f = csv.reader(f, delimiter=';')
        dates = []
        act_amount = []
        for c, row in enumerate(f):
            if c == 0:
                continue
            dates.append(row[0])
            act_amount.append(row.count('|'))
        # Calculate the average activation per minute
        act_amount = [sum(act_amount[i:i+600])//600 for i in range(0,len(act_amount),600)]
        # Get the dates with a minute interval
        dates = dates[0::600]
        x_val = [datetime.datetime.strptime(d,'%d-%m-%Y %H:%M:%S.%f') for d in dates]
        y_val = act_amount

        # Create graph with the hours
        ax = plt.gca()
        formatter = mdates.DateFormatter("%H")
        ax.xaxis.set_major_formatter(formatter)
        locator = mdates.HourLocator()
        ax.xaxis.set_major_locator(locator)
        plt.plot(x_val, y_val)
        plt.xlabel("Hours")
        plt.ylabel("Average activations per minute")
        plt.show()

def csv2pd(filename):
    df = pd.read_csv(f"../{filename}", delimiter=";", low_memory=True)
    return df

def trackCar(time, drivelane):
    """
    Tracks one car between 2 given times
    :param time:
    :param drivelane: input integer from drivelane name
    :return:
    """
    rijbanen = {1 : ['F055','011', '012', '013', '014'],
    3 : ['031', '032', '033', '034'],
    4 : ['041', '042', '043', '044'],
    5 : ['F055','051', '052', '053', '054'],
    11 : ['111', '112', '113', '114'],
    12 : ['121', '122', '123', '124'],
    41 : ['411', '412']}

    df = csv2pd('BOS210.csv')
    # reverse columns list for finding consequtive first activation sensor
    columns = rijbanen[drivelane][::-1]
    # time is added for showing time in dataframe
    rijbanen[drivelane].insert(0, 'time')
    # shows only rows after given time
    df1 = df[rijbanen[drivelane]][(df['time'] >= time)]

    car = dict()
    # df2 = df1[]

    for column in columns:
        tijd = df1["time"][(df1[column] == "|")]
        car[tijd.iloc[0]] = column

    with open('../data/one_car_trak.json', 'w') as json_file:
        json.dump(car, json_file)

# trackCar('08-01-2021 00:02:30.3', 11)
















