'''
Calculates the points table for the competition
'''
#%%
import pandas as pd
from resultAccumulator import *

# Get the team table
teamResults = AccumulateResults()

# Get the draw
filename = 'draw.csv'
draw = pd.read_csv(filename)

# Create the table
resultsTable = pd.DataFrame(columns=teamResults.columns[1:], index=draw.columns)

for person in draw.columns:
    resultsTable.loc[person] = teamResults[teamResults.index.isin(draw[person])].sum(axis=0).round(2)[1:]

resultsTable.sort_values('Total', ascending=False).to_csv('ResultsTable.csv')
