import pandas as pd
import json


def read_file(filename):
    """
    Leest .csv uit, en maakt een dataframe.

    :return pandas.DataFrame
    """
    df = pd.read_csv(f'../{filename}', delimiter=';', low_memory=False)
    return df


def to_dict():
    """
    Zet het aantal activaties in een Dictionary met de juiste rijbaan als key.

    :return dict, dict
    """
    bos210_dict = {
        "1": b210_amount011[0],
        "3": b210_amount031[0],
        "4": b210_amount041[0],
        "5": b210_amount051[0],
        "11": b210_amount111[0],
        "12": b210_amount121[0]
    }

    bos211_dict = {
        "5": amount051[0] + amount052[0],
        "6": amount061[0],
        "7": amount071[0],
        "9": amount091[0],
        "10": amount101[0],
        "11": amount111[0] + amount112[0]
    }
    return bos210_dict, bos211_dict


def kansberekening(bos210, bos211):
    """"
    Berekent de verhouding van de distributie van auto's die van één richting komen.

    :return dict, dict
    """
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



def main():
    dict210, dict211 = to_dict()

    k_210, k_211 = kansberekening(dict210, dict211)

    with open('kansen210.json', 'w') as json_file:
        json.dump(k_210, json_file)

    with open('kansen211.json', 'w') as json_file:
        json.dump(k_211, json_file)


# BOS210
df_210 = read_file('BOS210.csv')

b210_amount011 = df_210['011'].value_counts().tolist()
b210_amount031 = df_210['031'].value_counts().tolist()

b210_amount041 = df_210['041'].value_counts().tolist()
b210_amount051 = df_210['051'].value_counts().tolist()

b210_amount111 = df_210['111'].value_counts().tolist()
b210_amount121 = df_210['121'].value_counts().tolist()

# print(f"Activaties op rijbaan 1: {b210_amount011[0]}")
# print(f"Activaties op rijbaan 3: {b210_amount031[0]}")
# print(f"Activaties op rijbaan 4: {b210_amount041[0]}")
# print(f"Activaties op rijbaan 5: {b210_amount051[0]}")
# print(f"Activaties op rijbaan 11: {b210_amount111[0]}")
# print(f"Activaties op rijbaan 12: {b210_amount121[0]}")


# BOS211
df_211 = read_file('BOS211.csv')

amount051 = df_211['051'].value_counts().tolist()
amount052 = df_211['052'].value_counts().tolist()
amount061 = df_211['061'].value_counts().tolist()

amount071 = df_211['071'].value_counts().tolist()
amount091 = df_211['091'].value_counts().tolist()

amount101 = df_211['101'].value_counts().tolist()
amount111 = df_211['111'].value_counts().tolist()
amount112 = df_211['112'].value_counts().tolist()

# print(f"Activaties op rijbaan 5: {amount051[0] + amount052[0]}")
# print(f"Activaties op rijbaan 6: {amount061[0]}")
#
# print(f"Activaties op rijbaan 7: {amount071[0]}")
# print(f"Activaties op rijbaan 9: {amount091[0]}")
#
# print(f"Activaties op rijbaan 10: {amount101[0]}")
# print(f"Activaties op rijbaan 11: {amount111[0] + amount112[0]}")

if __name__ == '__main__':
    main()
