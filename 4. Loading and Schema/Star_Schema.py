# Import Libraries required for Processing
import pandas as pd
import numpy as np

# Setting file names used during execution process
# Input File :  Ball_By_Ball and Player_match Information CSV file consists of raw information about Matches
#               and its players along with the details like winning, scores and other factors
Player_match_file = 'transformed/Player_match.csv'
Ball_By_Ball_file = 'transformed/Ball_By_Ball.csv'

# Output File : ball_by_ball.csv file will hold the factual information of about matches in detail
#               player.csv file will hold only the Player Information.
#               match file will hold only the Match Information.
#               player_match.csv will hold only the Match and players associated with it Information.
#               role.csv file will hold only the Player roles Information.
#               batting_style.csv file will hold only the Player roles Information.
#               bowling_style.csv file will hold only the Player roles Information.
#               country.csv file will hold only the Player roles Information.
#               team.csv file will hold only the Player roles Information.
file_BallByBall_output = 'load/ball_by_ball.csv'
file_player_output = 'load/player.csv'
file_match_output = 'load/match.csv'
file_player_match_output = 'load/player_match.csv'
file_role_output = 'load/role.csv'
file_batting_style_output = 'load/batting_style.csv'  
file_bowling_style_output = 'load/bowling_style.csv'
file_country_output = 'load/country.csv'
file_team_output = 'load/team.csv'

# Reading the input CSV files
raw_player_match = pd.read_csv(Player_match_file)

raw_ball_df = pd.read_csv(Ball_By_Ball_file)

# Creating role dictionary
Role = {
   'role_id': ['1', '2', '3', '4'],
   'role_desc': ['Captain', 'Keeper', 'Player', 'CaptainKeeper']
}

#Converting role dictionary into dataframe to create role dimension table
Role_df = pd.DataFrame(Role)

# Creating Batting_Style dictionary
Batting_Style = {
   'batting_id': ['1', '2'],
   'batting_hand': ['Left-hand bat', 'Right-hand bat']
}

#Converting Batting_Style dictionary into dataframe to create Batting_Style dimension table
Batting_Style_df = pd.DataFrame(Batting_Style)

# Creating Bowling_Style dictionary
Bowling_Style = {
   'bowling_id': ['1', '2', '3', '4', '5','6', '7', '8', '9','10', '11', '12', '13', '14'],
   'bowling_skill': ['Right-arm medium', 'Right-arm offbreak', 'Right-arm fast-medium', 'Legbreak googly', 'Right-arm medium-fast',
                     'Left-arm fast-medium','Slow left-arm orthodox','Slow left-arm chinaman','Left-arm medium-fast',
                    'Legbreak','Right-arm fast','Right-arm bowler','Left-arm medium','Left-arm fast']
}

#Converting Bowling_Style dictionary into dataframe to create Bowling_Style dimension table
Bowling_Style_df = pd.DataFrame(Bowling_Style)

# Creating Country dictionary
Country = {
   'country_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
   'country_name': ['India', 'South Africa', 'U.A.E', 'New Zealand', 'Australia','Pakistan','Sri Lanka','West Indies',
                     'Zimbabwea','England','Bangladesh','Netherlands']
}

#Converting Country dictionary into dataframe to create Country dimension table
Country_df = pd.DataFrame(Country)

# Creating Team dictionary
Team = {
   'team_id': [1, 2, 3, 4, 5,6, 7, 8, 9, 10, 11, 12, 13],
   'team_name': ['Kolkata Knight Riders','Royal Challengers Bangalore','Chennai Super Kings',
                 'Kings XI Punjab','Rajasthan Royals','Delhi Daredevils','Mumbai Indians',
                 'Deccan Chargers','Kochi Tuskers Kerala','Pune Warriors','Sunrisers Hyderabad',
                 'Rising Pune Supergiants','Gujarat Lions']
}

#Converting Team dictionary into dataframe to create Team dimension table
Team_df = pd.DataFrame(Team)


def Batting_Skill(value):
    ''' This function returns batting id for the input value batting_hand'''
    return Batting_Style_df.loc[Batting_Style_df['batting_hand'] == value, 'batting_id'].iloc[0]

def Bowling_Skill(value):
    ''' This function returns bowling_id for the input value bowling_skill '''
    return Bowling_Style_df.loc[Bowling_Style_df['bowling_skill'] == value, 'bowling_id'].iloc[0]

def Country(value):
    ''' This function returns country_id for the input value country_name '''
    return Country_df.loc[Country_df['country_name'] == value, 'country_id'].iloc[0]

def role(value):
    ''' This function returns role_id for the input value role_desc '''
    return Role_df.loc[Role_df['role_desc'] == value, 'role_id'].iloc[0]

def team(value):
    ''' This function returns team_id for the input value team_name '''
    return Team_df.loc[Team_df['team_name'] == value, 'team_id'].iloc[0]

# Export the Star Schema and save them in CSV File respectively
# Save the Pre-Processed role DataFrame into a CSV file 
Role_df.to_csv(file_role_output, encoding='utf-8', index=False)

# Save the Pre-Processed batting_style DataFrame into a CSV file 
Batting_Style_df.to_csv(file_batting_style_output, encoding='utf-8', index=False)

# Save the Pre-Processed bowling_style DataFrame into a CSV file 
Bowling_Style_df.to_csv(file_bowling_style_output, encoding='utf-8', index=False)

# Save the Pre-Processed country DataFrame into a CSV file 
Country_df.to_csv(file_country_output, encoding='utf-8', index=False)

# Save the Pre-Processed team DataFrame into a CSV file 
Team_df.to_csv(file_team_output, encoding='utf-8', index=False)

# Creating Schema for Player dataset
df_players = raw_player_match.loc[ : , ['Player_Id', 'Player_Name', 'DOB', 'Batting_hand', 'Bowling_skill', 'Country_Name']]

df_players = df_players.sort_values(by = ['Player_Id'], ascending = True, na_position = 'last').drop_duplicates(['Player_Id'],keep = 'first')

df_players['Bowling_skill'] = df_players.apply(lambda row: Bowling_Skill(row['Bowling_skill']),axis=1)
df_players['Batting_hand'] = df_players.apply(lambda row: Batting_Skill(row['Batting_hand']),axis=1)
df_players['Country_Name'] = df_players.apply(lambda row: Country(row['Country_Name']),axis=1)

# Save the Pre-Processed players DataFrame into a CSV file 
df_players.to_csv(file_player_output, encoding='utf-8', index=False)


# Creating Schema for Player_Match dataset
df_player_match = raw_player_match.loc[ : , ['Match_Id', 'Player_Id', 'Role_Desc','Player_team']]

df_player_match = df_player_match.sort_values(by = ['Player_Id'], ascending = True, na_position = 'last').drop_duplicates(['Player_Id'],keep = 'first')

df_player_match['Role_Desc'] = df_player_match.apply(lambda row: role(row['Role_Desc']),axis=1)
df_player_match['Player_team'] = df_player_match.apply(lambda row: team(row['Player_team']),axis=1)
print(df_player_match)

# Export the Star Schema and save Player Match in CSV File respectively
df_player_match.to_csv(file_player_match_output, encoding='utf-8', index=False)

df_match = raw_player_match.loc[ : , ['Match_Id', 'Player_team', 'Opposit_Team', 'Season_year', 'Venue_Name', 'City_Name',
                                     'Country_Name','Toss_Winner','Toss_Name','Win_Type','Outcome_Type','Win_Margin']]

df_match = df_match.sort_values(by = ['Match_Id'], ascending = True, na_position = 'last').drop_duplicates(['Match_Id'],keep = 'first')

df_match['Player_team'] = df_match.apply(lambda row: team(row['Player_team']),axis=1)
df_match['Opposit_Team'] = df_match.apply(lambda row: team(row['Opposit_Team']),axis=1)

# Export the Star Schema and save Match in CSV File respectively
df_match.to_csv(file_match_output, encoding='utf-8', index=False)

df_ball = raw_ball_df.loc[ : , ['MatcH_id', 'Over_id', 'Ball_id', 'Innings_No', 'Team_Batting', 'Team_Bowling',
                                     'Striker_Batting_Position','Striker','Non_Striker','Bowler']]

df_ball['Team_Batting'] = df_ball.apply(lambda row: team(row['Team_Batting']),axis=1)
df_ball['Team_Bowling'] = df_ball.apply(lambda row: team(row['Team_Bowling']),axis=1)
print(df_ball)

# Export the Star Schema and save Ball_by_Ball in CSV File respectively
df_ball.to_csv(file_BallByBall_output, encoding='utf-8', index=False)

