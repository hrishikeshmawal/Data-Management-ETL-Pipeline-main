# Import Libraries required for Processing
import pandas as pd
from pandas_profiling import ProfileReport
import pandas_profiling

def main():
    # Setting file names used during execution process
    # Input File :  Ball_By_Ball and Player_match Information CSV file consists of raw information about Matches
    #               and its players along with the details like winning, scores and other factors
    Raw_Player_match_file = 'Raw_Player_match.csv'
    Raw_Ball_By_Ball_file = 'Raw_Ball_By_Ball.csv'

    # read the file
    Ball_df_input = pd.read_csv(Raw_Ball_By_Ball_file)

    # run the profile report
    profile = Ball_By_Ball_df.profile_report(title='Pandas Profiling Report')

    # save the report as html file
    profile.to_file(output_file="output/pandas_profiling_Ball_By_Ball.html")

    # read the file
    Player_match_df = pd.read_csv('Raw_Player_match.csv',encoding= 'unicode_escape')

    # run the profile report
    profile = Player_match_df.profile_report(title='Pandas Profiling Player Match Report')


    # save the report as html file
    profile.to_file(output_file="outout/pandas_profiling_player_match.html")

    ## Output of the pandas profiling has been stored in output folder

if __name__ == "__main__":
    main()

