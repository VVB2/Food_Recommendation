import pandas as pd

df = pd.read_csv("recipes_data.csv", nrows=15000)

df = df.drop_duplicates(subset=["title"])

df["title"] = df["title"].str.strip()

pd.DataFrame(df).to_csv("minified_data.csv", index=False, mode='w')