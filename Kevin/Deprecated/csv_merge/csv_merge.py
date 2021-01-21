"""
Dit bestand werd gebruikt om BOS210 en BOS211 data samen te voegen.
We hadden uiteindelijk niet genoeg tijd om BOS211 ook te doen, dit
bestand is dus niet langer nodig.
"""

import pandas as pd


def readfile(filename):
    """
    Leest een csv bestand uit.

    :return DataFrame
    """
    df = pd.read_csv(f"../{filename}", delimiter=";", low_memory=False)
    return df


def rename_columns(datafr, prefix):
    """
    Hernoem de kolommen zodat je weet welke kolom voor welke rijbaan is
    (bijvoorbeeld: b210_011, b210_012, b211_101, b211_102, etc.)

    :return DataFrame
    """
    datafr = datafr.rename(lambda x: prefix+x, axis='columns')

    return datafr


def main():
    b210 = rename_columns(readfile('BOS210.csv'), "b210_")
    b211 = rename_columns(readfile('BOS211.csv'), "b211_")

    mergeDF = b210.join(b211.set_index('b211_time'), on='b210_time')

    mergeDF.to_csv("MergedData.csv", sep=",")
    print(mergeDF)


if __name__ == '__main__':
    main()
