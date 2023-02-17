import pandas as pd
rocks_df = pd.read_csv('~/Desktop/hyperskill-dataset-71537193.txt')
print(rocks_df.head())
print(pd.pivot_table(rocks_df, index= 'labels', values= 'null_deg', aggfunc='mean', ).round(2).loc['R'][0])
