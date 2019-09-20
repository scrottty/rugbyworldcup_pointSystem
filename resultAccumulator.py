'''
Accumulates the results into a table with points for each team across the points
'''

#%%
import pandas as pd

cols = ['Tier', 'Win', 'Lose', 'NumTackles', 'Passes', 'Meters', 'Breaks', 'DropGoals', 'Yellows', 'Reds']
tier1 = ['Ireland', 'New Zealand', 'South Africa', 'England', 'Argentina', 'Australia', 'Wales', 'France']
tier2 = ['Scotland', 'Japan', 'Italy', 'USA', 'Fiji', 'Georgia', 'Samoa', 'Tonga']
tier3 = ['Romania', 'Namibia', 'Canada', 'Uruguay']

teams = pd.DataFrame(columns=cols, index=tier1+tier2+tier3).fillna(0)

teams.loc[tier1, 'Tier'] = 1
teams.loc[tier2, 'Tier'] = 2
teams.loc[tier3, 'Tier'] = 3

teams.sort_index(inplace=True)

# Load in the matches
filename = "Matches.csv"
matches = pd.read_csv(filename)
matches.replace("United States of America", "USA", inplace=True)
matches.set_index('TeamName', inplace=True)


# Loop through each match and calculate that teams points
# matches = matches[(matches.index == 'Namibia') | (matches['Opponent'] == 'Namibia')]
for idx, match in matches.iterrows():
    team = match.name
    # Get both match results
    match = matches.loc[matches['MatchID']==match.loc['MatchID']]

    # Win or Draw Calc
    tierby1 = (teams.loc[team, 'Tier'] - teams.loc[match.loc[team, 'Opponent'], 'Tier']) > 0
    tierby2 = (teams.loc[team, 'Tier'] - teams.loc[match.loc[team, 'Opponent'], 'Tier']) > 1
    win = match.loc[team,'PointsFor'] >= match.loc[team, 'PointsAgainst']
    teams.loc[team ,'Win'] += 2 * win + 2 * tierby1 * win + 6 * tierby2 * win

    # Lose Points
    lose = (match.loc[team,'PointsFor'] > match.loc[team, 'PointsAgainst'] - 7) & ~win
    teams.loc[team ,'Lose'] += 1 * lose + 1 * tierby1 * lose + 3 * tierby2 * lose

    # Tackle %
    # teams.loc[team ,'Tackle%'] += 2 * match.loc[team, 'Tackle%']

    # Propotional Points
    for col in cols[3:7]:
        total = (match.loc[team, col]+ match.loc[match.loc[team, 'Opponent'],col])
        if total > 0:
            teams.loc[team ,col] += 2 * (match.loc[team, col] / total)

    # Drop Goals
    teams.loc[team, 'DropGoals'] += match.loc[team, 'DropGoals']

    # Yellows
    yellows = match.loc[team, 'Yellows']
    teams.loc[team, 'Yellows'] -= yellows

    # Reds
    teams.loc[team, 'Reds'] -= match.loc[team, 'Reds'] * 2

# Calculate Totals
teams['Total'] = teams[cols[1:]].sum(axis=1)


#%%
