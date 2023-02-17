import pandas as pd
data = pd.read_csv('~/Desktop/hyperskill-dataset-71476628.txt')

data.dropna(thresh=7, axis=1, inplace=True)
print(data)
median = data.median()
data.fillna(median, inplace=True)

print(data.head(5))
