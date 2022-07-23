# Import Libraries required for Processing
import pandas as pd

# Input file
file_input = 'input data/Raw_Ball_by_Ball.csv'

# Location to store processed file
file_pre_processed = 'Staging/Ball_By_Ball.csv'

# Reading the input Ball_by_Ball CSV file
Ball_by_Ball_df = pd.read_csv(file_input)

# Cleaning the Team_Batting columns by replacing duplicate and incorrect values
Ball_by_Ball_df['Team_Batting'].unique()
Ball_by_Ball_df['Team_Batting'] = Ball_by_Ball_df['Team_Batting'].str.replace('Rising_Pune_Supergiants','Rising Pune Supergiants')
Ball_by_Ball_df['Team_Batting'] = Ball_by_Ball_df['Team_Batting'].str.replace('Sunrisers-Hyderabad','Sunrisers Hyderabad')
Ball_by_Ball_df['Team_Batting'] = Ball_by_Ball_df['Team_Batting'].str.replace('GujaratLions','Gujarat Lions')

# Cleaning the Team_Bowling columns by replacing duplicate and incorrect values
Ball_by_Ball_df['Team_Bowling'].unique()
Ball_by_Ball_df['Team_Bowling'] = Ball_by_Ball_df['Team_Bowling'].str.replace('Rising_Pune_Supergiants','Rising Pune Supergiants')
Ball_by_Ball_df['Team_Bowling'] = Ball_by_Ball_df['Team_Bowling'].str.replace('Sunrisers-Hyderabad','Sunrisers Hyderabad')
Ball_by_Ball_df['Team_Bowling'] = Ball_by_Ball_df['Team_Bowling'].str.replace('GujaratLions','Gujarat Lions')

# Cleaning the Batsman_Runs_Scored columns by replacing invalid value -1 to 0
Ball_by_Ball_df['Batsman_Runs_Scored'].unique()
Ball_by_Ball_df['Batsman_Runs_Scored'] = Ball_by_Ball_df['Batsman_Runs_Scored'].astype(str)
Ball_by_Ball_df['Batsman_Runs_Scored'] = Ball_by_Ball_df['Batsman_Runs_Scored'].str.replace('-1','0')
Ball_by_Ball_df['Batsman_Runs_Scored'] = Ball_by_Ball_df['Batsman_Runs_Scored'].astype('int64')

# Cleaning the Extra_Type columns by replacing duplicate and incorrect values
Ball_by_Ball_df['Extra_Type'].unique()
Ball_by_Ball_df['Extra_Type'] = Ball_by_Ball_df['Extra_Type'].str.replace('wites','Wides')
Ball_by_Ball_df['Extra_Type'] = Ball_by_Ball_df['Extra_Type'].str.replace('Byes','byes')
Ball_by_Ball_df['Extra_Type'] = Ball_by_Ball_df['Extra_Type'].str.replace('Legbyes','legbyes')
Ball_by_Ball_df['Extra_Type'] = Ball_by_Ball_df['Extra_Type'].str.replace('Noballs','noballs')
Ball_by_Ball_df['Extra_Type'] = Ball_by_Ball_df['Extra_Type'].str.replace('Wides','wides')

# Cleaning the inconsistent values of match date
Ball_by_Ball_df['Match_Date'].head
Ball_by_Ball_df['Match_Date'].unique()
Ball_by_Ball_df['Match_Date'] = pd.to_datetime(Ball_by_Ball_df['Match_Date']).dt.strftime('%d-%m-%Y')
Ball_by_Ball_df['Match_Date'] = pd.to_datetime(Ball_by_Ball_df['Match_Date'])

# Cleaning the duplicate value with same meaning in Out_type column
Ball_by_Ball_df['Out_type'] = Ball_by_Ball_df['Out_type'].str.replace('Keeper Catch','caught')

# One hot encoding the values of Extra_Type column to analyse it get the integer values
Ball_by_Ball_df = pd.concat([Ball_by_Ball_df, pd.get_dummies(Ball_by_Ball_df.Extra_Type)], 1)

# One hot encoding the values of Out_type column to analyse it get the integer values
Ball_by_Ball_df = pd.concat([Ball_by_Ball_df, pd.get_dummies(Ball_by_Ball_df.Out_type)], 1)

# Creating new derived column Extra_runs by combining the values of other columns wides, legbyes, byes, noballs, penalty
Ball_by_Ball_df['Extra_runs'] = Ball_by_Ball_df['wides'] + Ball_by_Ball_df['legbyes'] + Ball_by_Ball_df['byes'] + Ball_by_Ball_df['noballs'] +  Ball_by_Ball_df['penalty']

# Creating new derived column Bowler_Extras by combining the values of other columns wides and noballs
Ball_by_Ball_df['Bowler_Extras'] = Ball_by_Ball_df['wides'] + Ball_by_Ball_df['noballs']


def Out_type(row):
    ''' This function returns the value as 0 when following Out-type are occured
        in this case bowler does not get any runs hence 0 has been returnedand for values othern than the following 1 is returned'''
    if row['Out_type'] == 'Not Applicable': 
        return 0
    elif row['Out_type'] == 'obstructing the field':
        return 0
    elif row['Out_type'] == 'retired hurt':
        return 0
    elif row['Out_type'] == 'run out':
        return 0                              
    return 1

## Creating derived column 'Bowler_Wicket' to store the total runs scored by bowler
Ball_by_Ball_df['Bowler_Wicket'] = Ball_by_Ball_df.apply(lambda row: Out_type(row),axis=1)

## Selecting the required column and storing it in dataframe for further processing
Ball_by_Ball_df = Ball_by_Ball_df[['MatcH_id','Over_id','Ball_id','Innings_No','Team_Batting','Team_Bowling', 'Striker_Batting_Position','Extra_Type',
                                   'Batsman_Runs_Scored','Extra_runs','wides','legbyes','byes','noballs','penalty','Bowler_Extras',
                                   'Out_type', 'caught','bowled','run out','lbw','retired hurt','stumped', 'caught and bowled','hit wicket',
                                   'obstructing the field', 'Bowler_Wicket','Match_Date', 'Striker','Non_Striker', 'Bowler', 'Player_Out', 'Fielders']]


## Staging the file after processing/cleaning it the transformation stage
Ball_by_Ball_df.to_csv(file_pre_processed, encoding='utf-8', index=False)


