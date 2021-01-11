import pandas as pd
import json


# Leest .csv uit, en maakt een dataframe.
def read_file(filename):
    df = pd.read_csv(filename, delimiter=';', low_memory=False)
    df = df.fillna("0")
    return df


def to_dict():
    bos210_dict = {
        "1": b210_amount011[1],
        "3": b210_amount031[1],
        "4": b210_amount041[1],
        "5": b210_amount051[1],
        "11": b210_amount111[1],
        "12": b210_amount121[1]
    }

    bos211_dict = {
        "5": amount051[1] + amount052[1],
        "6": amount061[1],
        "7": amount071[1],
        "9": amount091[1],
        "10": amount101[1],
        "11": amount111[1] + amount112[1]
    }
    return bos210_dict, bos211_dict


def kansberekening(bos210, bos211):
    # BOS210
    bos210_baan_1 = bos210['1'] / (bos210['1'] + bos210['3'])
    bos210_baan_3 = 1 - bos210_baan_1

    bos210_baan_4 = bos210['4'] / (bos210['4'] + bos210['5'])
    bos210_baan_5 = 1 - bos210_baan_4

    bos210_baan_11 = bos210['11'] / (bos210['11'] + bos210['12'])
    bos210_baan_12 = 1 - bos210_baan_11

    kansen_210 = {
        "1": bos210_baan_1,
        "3": bos210_baan_3,
        "4": bos210_baan_4,
        "5": bos210_baan_5,
        "11": bos210_baan_11,
        "12": bos210_baan_12
    }

    # BOS211
    bos211_baan_5 = bos211['5'] / (bos211['5'] + bos211['6'])
    bos211_baan_6 = 1 - bos211_baan_5

    bos211_baan_7 = bos211['7'] / (bos211['7'] + bos211['9'])
    bos211_baan_9 = 1 - bos211_baan_7

    bos211_baan_10 = bos211['10'] / (bos211['10'] + bos211['11'])
    bos211_baan_11 = 1 - bos211_baan_10

    kansen_211 = {
        "5": bos211_baan_5,
        "6": bos211_baan_6,
        "7": bos211_baan_7,
        "9": bos211_baan_9,
        "10": bos211_baan_10,
        "11": bos211_baan_11
    }

    return kansen_210, kansen_211


# BOS210
b210_amount011 = read_file('BOS210.csv')['011'].value_counts().tolist()
b210_amount031 = read_file('BOS210.csv')['031'].value_counts().tolist()

b210_amount041 = read_file('BOS210.csv')['041'].value_counts().tolist()
b210_amount051 = read_file('BOS210.csv')['051'].value_counts().tolist()

b210_amount111 = read_file('BOS210.csv')['111'].value_counts().tolist()
b210_amount121 = read_file('BOS210.csv')['121'].value_counts().tolist()

print(f"Activaties op rijbaan 1: {b210_amount011[1]}")
print(f"Activaties op rijbaan 3: {b210_amount031[1]}")
print(f"Activaties op rijbaan 4: {b210_amount041[1]}")
print(f"Activaties op rijbaan 5: {b210_amount051[1]}")
print(f"Activaties op rijbaan 11: {b210_amount111[1]}")
print(f"Activaties op rijbaan 12: {b210_amount121[1]}")


# BOS211
amount051 = read_file('BOS211.csv')['051'].value_counts().tolist()
amount052 = read_file('BOS211.csv')['052'].value_counts().tolist()
amount061 = read_file('BOS211.csv')['061'].value_counts().tolist()

amount071 = read_file('BOS211.csv')['071'].value_counts().tolist()
amount091 = read_file('BOS211.csv')['091'].value_counts().tolist()

amount101 = read_file('BOS211.csv')['101'].value_counts().tolist()
amount111 = read_file('BOS211.csv')['111'].value_counts().tolist()
amount112 = read_file('BOS211.csv')['112'].value_counts().tolist()

print(f"Activaties op rijbaan 5: {amount051[1] + amount052[1]}")
print(f"Activaties op rijbaan 6: {amount061[1]}")

print(f"Activaties op rijbaan 7: {amount071[1]}")
print(f"Activaties op rijbaan 9: {amount091[1]}")

print(f"Activaties op rijbaan 10: {amount101[1]}")
print(f"Activaties op rijbaan 11: {amount111[1] + amount112[1]}")


dict210, dict211 = to_dict()

k_210, k_211 = kansberekening(dict210, dict211)

with open('kansen210.json', 'w') as json_file:
    json.dump(k_210, json_file)

with open('kansen211.json', 'w') as json_file:
    json.dump(k_211, json_file)
