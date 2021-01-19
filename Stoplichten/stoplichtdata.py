import pandas as pd
import json

with open('b210_stoplicht.json') as jf:
    data = json.load(jf)

df = pd.json_normalize(data)

print(df)
