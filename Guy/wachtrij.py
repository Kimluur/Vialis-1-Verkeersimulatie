import json
import pandas as pd
import numpy as np
from Guy.Vialis_Functies import csv2pd
from tqdm import tqdm

def wachtrij():
    rijbanen = [['01','011'],
                ['03', '031'],
                ['04', '041'],
                ['05', '051'],
                ['11', '111'],
                ['12', '121'],
                ['41', '411']]


    df = csv2pd('BOS210.csv')

    for i in rijbanen:
        # print(f"{i[0]}: " + tel(df[i[1]]))
        return


def tel(df1):
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

wachtrij()