import pandas as pd
from datetime import timedelta


def add_hour(datafr):
    """Deze functie voegt 1 uur toe aan elke timestamp binnen onze eigen GPS data
    Door een fout in het GPS programma liep de tijd in de CSV overal 1 uur achter."""
    datafr.timestamp = pd.DatetimeIndex(datafr.timestamp) + timedelta(hours=1)


def fill_coords(datafr):
    """Onze GPS hield niet met een vast interval onze locatie bij, sons skipte hij 23 seconde omdat we stil stonden.
    Om dit soort gaten op te vullen hebben we doormiddel van interpolatie berekend waar we op elk moment waren.
    Zodat de interval tussen elke stap 0.1 seconde word. Pandas heeft een ingebouwde interpolate functie."""
    datafr.interpolate(method='quadratic', inplace=True)

    return datafr


def fix_timestamp(datafr):
    """Na de interpolatie stonden er 6 0en achter de komma bij de seconde. Met deze functie halen we deze weg."""
    datafr['timestamp'] = datafr['timestamp'].str.slice(stop=21)


def main_dataframe():
    """Deze functie returnt een dataframe met daarin de GPS locatie van onze eigen auto op elke 0.1 seconde"""
    # Lees CSV
    df = pd.read_csv('data/car_data.csv', delimiter=";")

    # Converteer 'timestamp' om naar datetime
    df.timestamp = df.timestamp.str.slice(stop=19)

    # Voeg één uur toe aan tijd, als correctie
    add_hour(df)

    # Vul tijden in met milliseconden
    df = df.set_index('timestamp').resample("100ms").first().reset_index().reindex(columns=df.columns)
    cols = df.columns.difference(
        ['latitude', 'longitude', 'speed'])
    df[cols] = df[cols].ffill()

    # Zet tijd in juiste format
    df['timestamp'] = df["timestamp"].dt.strftime("%d-%m-%Y %H:%M:%S.%f")
    df = fill_coords(df)
    fix_timestamp(df)

    return df
