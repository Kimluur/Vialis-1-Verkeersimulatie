import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
    Reads csv to see how long an activation is and with the distance that TODO: add distance variable
    calculates the velocity in km/h
    :return: velocity in km/h
    """
    sensor = []
    activation = False
    with open('BOS210_Correct.csv') as f:
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

# 02-11-2020 00:00:00.0
def busy_graph():
    """
    Creates graph that points out what times are busy on the intersection
    :return: Matplotlib graph
    """
    with open('BOS210_Correct.csv') as f:
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


busy_graph()

