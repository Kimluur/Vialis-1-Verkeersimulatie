import csv

def velocity():
    sensor = []
    activation = False
    with open('BOS210_Correct.csv') as f:
        r = csv.reader(f, delimiter=';')
        for i in r:
            if i[38] == '|' and activation == False:
                sensor.append(i[38])
                activation = True
            elif i[38] == '|' and activation == True:
                sensor.append(i[38])
            elif i[38] == '' and activation == True:
                activation = False
                break
    return sensor

print(velocity())