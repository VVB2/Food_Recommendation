import pandas as pd

df = pd.read_csv('data/minified_data.csv', nrows=100)

# df['ingredients'] = df['ingredients'].astype('list')

for data in df.itertuples(index=False):
    ingredients = getattr(data,'ingredients')