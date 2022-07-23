# Import Libraries required for Processing
import pandas as pd

# Input file
file_input = 'input data/Raw_Player_match.csv'

# Location to store processed file
file_pre_processed = 'Staging/Player_match.csv'

# Reading the input Raw_Player_match CSV file
Player_match_df = pd.read_csv(file_input,encoding= 'unicode_escape')

# Implementing basic steps to understand the data
Player_match_df.shape

Player_match_df.columns

Player_match_df.dtypes

# Cleaning the Batting_hand columns by replacing duplicate and incorrect values
Player_match_df['Batting_hand'].unique()
Player_match_df['Batting_hand'] = Player_match_df['Batting_hand'].str.replace('Right-hand bat','Right-hand-bat')
Player_match_df['Batting_hand'] = Player_match_df['Batting_hand'].str.replace('\xa0Right-hand bat','Right-hand-bat')
Player_match_df['Batting_hand'] = Player_match_df['Batting_hand'].str.replace('Right-handed','Right-hand-bat')
Player_match_df['Batting_hand'] = Player_match_df['Batting_hand'].str.replace('Left-hand bat','Left-hand-bat')
Player_match_df['Batting_hand'] = Player_match_df['Batting_hand'].str.replace('\xa0Left-hand bat','Left-hand-bat')

# Cleaning the Bowling_skill columns by replacing duplicate and incorrect values
Player_match_df['Bowling_skill'].unique()
Player_match_df['Bowling_skill'] = Player_match_df['Bowling_skill'].str.replace('\xa0Right-arm offbreak','Right-arm offbreak')
Player_match_df['Bowling_skill'] = Player_match_df['Bowling_skill'].str.replace('\xa0Left-arm fast','Left-arm fast')
Player_match_df['Bowling_skill'] = Player_match_df['Bowling_skill'].str.replace('\xa0Right-arm fast-medium','Right-arm fast-medium')
Player_match_df['Bowling_skill'] = Player_match_df['Bowling_skill'].str.replace('\xa0Right-arm medium-fast','Right-arm medium-fast')
Player_match_df['Bowling_skill'] = Player_match_df['Bowling_skill'].str.replace('Right-arm medium fast','Right-arm medium-fast')
Player_match_df['Bowling_skill'] = Player_match_df['Bowling_skill'].str.replace('\xa0Legbreak','Legbreak')

# Cleaning the Toss_Winner columns by replacing duplicate and incorrect values
Player_match_df['Toss_Winner'].unique()
Player_match_df['Toss_Winner'] = Player_match_df['Toss_Winner'].str.replace('Sunshiners Hyderabad','Sunrisers Hyderabad')
Player_match_df['Toss_Winner'] = Player_match_df['Toss_Winner'].str.replace('Rising Pune Supergiant','Rising Pune Supergiants')

# Cleaning the Player_team columns by replacing duplicate and incorrect values
Player_match_df['Player_team'].unique()
Player_match_df['Player_team'] = Player_match_df['Player_team'].str.replace('Sunshiners Hyderabad','Sunrisers Hyderabad')
Player_match_df['Player_team'] = Player_match_df['Player_team'].str.replace('sunrisers Hyderabad','Sunrisers Hyderabad')
Player_match_df['Player_team'] = Player_match_df['Player_team'].str.replace('kings XI Punjab','Kings XI Punjab')

# Cleaning the Opposit_Team columns by replacing duplicate and incorrect values
Player_match_df['Opposit_Team'].unique()
Player_match_df['Opposit_Team'] = Player_match_df['Opposit_Team'].str.replace('Sunshiners Hyderabad','Sunrisers Hyderabad')


# Dropping the columns as they are completely empty
Player_match_df.drop(columns =["Batting_Status"], inplace = True)
Player_match_df.drop(columns =["Bowling_Status"], inplace = True)

## Staging the file after processing/cleaning it the transformation stage
Player_match_df.to_csv(file_pre_processed, encoding='utf-8', index=False)


