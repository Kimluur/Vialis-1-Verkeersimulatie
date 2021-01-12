import pandas as pd


def readfile(filename):
    df = pd.read_csv(f"../{filename}", delimiter=";", low_memory=False)
    return df


def rename_columns(datafr, prefix):
    datafr = datafr.rename(lambda x: prefix+x, axis='columns')

    return datafr


def main():
    b210 = rename_columns(readfile('BOS210.csv'), "b210_")
    b211 = rename_columns(readfile('BOS211.csv'), "b211_")

    mergeDF = b210.join(b211.set_index('b211_time'), on='b210_time')

    print(mergeDF)


if __name__ == '__main__':
    main()
