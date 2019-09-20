'''
Calculates the points table for the competition
'''
#%%
import pandas as pd

# Get the draw
filename = 'draw.csv'
draw = pd.read_csv(filename)

draw.replace('Russia', 'Romania', inplace=True)

#%%
resultsTable = pd.DataFrame(columns=teams.columns[1:], index=draw.columns)

#%%
for person in draw.columns:
    resultsTable.loc[person] = teams[teams.index.isin(draw[person])].sum(axis=0)[1:]

#%%
