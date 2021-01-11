import csv

def give_index(column_name):
    header = ['time', '01', '03', '04', '05', '11', '12', '22', '24', '28', '31', '32', '37', '38', '41', '011', '012', '013', '014', '031', '032', '033', '034', '041', '042', '043', '044', '051', '052', '053', '054', '111', '112', '113', '114', '121', '122', '123', '124', '221', '222', '223', 'K22', '241', 'K24', '281', 'K28', 'K311', 'K312321', 'K322', 'K371', 'K372381', 'K382', '411', '412', 'F055']
    print(header.index(column_name))

def velocity():
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

print(velocity())
give_index('013')



