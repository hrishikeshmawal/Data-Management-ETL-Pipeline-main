# Import Libraries required for Processing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from datetime import datetime
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#Models
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Input CSV files
file_input = 'data/Match.csv'
model_input1 = 'data/Player.csv'
model_input2 = 'data/Ball_By_Ball1.csv'


# Reading the input CSV files
Match_df = pd.read_csv(file_input)
Player_df = pd.read_csv(model_input , encoding= 'unicode_escape')
Ball_by_Ball_df = pd.read_csv(model_input2)

# Getting basic inforation about the dataset
print(Match_df.head)
print(Match_df.shape)
print(Match_df.columns)
print(Match_df.isna().sum())

# For optimizing the value replacing it with abbrevations
Match_df.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)
Match_df.fillna(np.NaN)


# Basic Visualizations performed on the dataset to answer below questions

print('1. Most Man of the Match Awards')

ManOfMatch = Match_df.iloc[:, 14]
players = ManOfMatch.value_counts().head(10).keys().tolist()
values = ManOfMatch.value_counts().head(10).tolist()
plt.gcf().set_size_inches(15,5)
plt.xlabel('Player')
plt.ylabel('Awards')
plt.title('Most Man of the match awards')
plt.barh(players, values, color = 'b', )
plt.gca().invert_yaxis()
plt.xlim(5, 20)
plt.show()

print('2. Likelihood of Toss determining win')

Toss_likelihood = Match_df.loc[:, ['Toss_Winner', 'match_winner']] #use loc instead of iloc as we use column labels
is_true = Toss_likelihood['Toss_Winner'] == Toss_likelihood['match_winner']
Toss_likelihood = Toss_likelihood[is_true]
percentage = (Toss_likelihood.shape[0]/Match_df.shape[0]) * 100
labels = ['Yes', 'No']
share = [percentage, 100 - percentage]
plt.pie(share, labels=labels,autopct='%1.1f%%', startangle=90)
plt.title('Toss determining Win')
my_circle=plt.Circle( (0,0), 0.3, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

print('3. Favourite Venues of the League')


Fav_Venue = Match_df.loc[:, ['Venue_Name']]
stadium = Fav_Venue['Venue_Name'].value_counts().head(15).keys().tolist()
values = Fav_Venue['Venue_Name'].value_counts().head(15).tolist()
plt.gcf().set_size_inches(15,5)
plt.xlabel('Stadium')
plt.ylabel('Matches hosted')
plt.title('Favourite Venues')
plt.bar(stadium, values, color = 'grey')
plt.gcf().autofmt_xdate()
plt.show()

print('4. Number of Matches played each season')

NoOfMatch = Match_df.iloc[:, 5]
season = NoOfMatch.value_counts().keys().tolist()
values = NoOfMatch.value_counts().tolist()
plt.gcf().set_size_inches(9,5)
plt.xlabel('Season')
plt.ylabel('Matches played')
plt.title('Matches played each season')
plt.bar(season, values, color = 'c')
plt.xticks(season)
plt.show()

## Data Preparation for modelling

Ball_by_Ball11 = Ball_by_Ball_df.loc[:, ['Striker', 'Runs_Scored']]

Ball_by_Ball = Ball_by_Ball11.groupby('Striker', as_index = False).sum()


Ball_by_Ball = Ball_by_Ball.sort_values(by=['Runs_Scored'], ascending = False)

batsman = Ball_by_Ball['Striker'].tolist()
runs = Ball_by_Ball['Runs_Scored'].tolist()

BbB_preprocessed = Ball_by_Ball_df.loc[:, ['Striker', 'Bowler', 'Out_type']]
Out_type = ['caught',
 'bowled',
 'run out',
 'lbw',
 'caught and bowled',
 'stumped',
 'hit wicket']

is_bowler = (BbB_preprocessed['Out_type'] == 'bowled') | (BbB_preprocessed['Out_type'] == 'caught') |
            (BbB_preprocessed['Out_type'] == 'caught and bowled') | (BbB_preprocessed['Out_type'] == 'stumped') |
            (BbB_preprocessed['Out_type'] == 'lbw') | (BbB_preprocessed['Out_type'] == 'hit wicket')


bowler_data = BbB_preprocessed[is_bowler].loc[:, ['Bowler']]


bowler = bowler_data['Bowler'].value_counts().keys().tolist()
wickets = bowler_data['Bowler'].value_counts().tolist()


d1 = {'Player_Id':bowler,'Wickets':wickets}
d2 = {'Player_Id':batsman,'Runs':runs}
df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)

df = pd.merge(df2,
                 df1,
                 on='Player_Id', how = 'left')
df.columns = ['Player_Id', 'Runs', 'Wickets']
df = df.fillna(0)

def calculate_age(born):
    born = datetime.strptime(born, "%m/%d/%Y").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

Player_df['Age'] = Player_df['DOB'].apply(calculate_age)
Player_df = Player_df.loc[:, ['Player_Id','Player_Name','Age','Batting_hand','Bowling_skill','Country_Name']]

print(Player_df)

Player_df.columns = ['Player_Id','Player', 'Age', 'Batting Skill', 'Bowling Skill', 'Country']
Merged_Player_df = pd.merge(df, Player_df, on = 'Player_Id')

print(Merged_Player_df)

def player_type(row):
    if row['Runs'] > 600  and row['Wickets'] > 25:
        return 'All Rounder'
    elif row['Runs'] > 600:
        return 'Batsman'
    elif row['Wickets'] > 25:
        return 'Bowler'                              
    return 'Other'

def player_rating(row):
    if row['Runs'] < 500:
        value_batting = 2
    elif row['Runs'] >= 500 and row['Runs'] < 1000:
        value_batting = 3
    elif row['Runs'] >= 1000 and row['Runs'] < 1500:
        value_batting = 4
    elif row['Runs'] >= 1500 and row['Runs'] < 2000:
        value_batting = 5
    elif row['Runs'] >= 2000 and row['Runs'] < 2500:
        value_batting = 6
    elif row['Runs'] >= 2500 and row['Runs'] < 3000:
        value_batting = 7
    elif row['Runs'] >= 3000 and row['Runs'] < 3500:
        value_batting = 8
    elif row['Runs'] >= 3500 and row['Runs'] < 4000:
        value_batting = 9
    elif row['Runs'] >= 4000:
        value_batting = 10
    if row['Wickets'] < 10:
        value_bowling = 2
    elif row['Wickets'] >= 10 and row['Wickets'] < 20:
        value_bowling = 3
    elif row['Wickets'] >= 20 and row['Wickets'] < 30:
        value_bowling = 4
    elif row['Wickets'] >= 30 and row['Wickets'] < 50:
        value_bowling = 5
    elif row['Wickets'] >= 50 and row['Wickets'] < 75:
        value_bowling = 6
    elif row['Wickets'] >= 75 and row['Wickets'] < 100:
        value_bowling = 7
    elif row['Wickets'] >= 100 and row['Wickets'] < 125:
        value_bowling = 8
    elif row['Wickets'] >= 125 and row['Wickets'] < 140:
        value_bowling = 9
    elif row['Wickets'] >= 140:
        value_bowling = 10
    if row['Age'] >= 35:
        age_value = 2
    elif row['Age'] >= 35 and row['Age'] < 40:
        age_value = 3
    elif row['Age'] >= 32 and row['Age'] < 35:
        age_value = 4
    elif row['Age'] >= 30 and row['Age'] < 32:
        age_value = 5
    elif row['Age'] >= 28 and row['Age'] < 30:
        age_value = 6
    elif row['Age'] >= 26 and row['Age'] < 28:
        age_value = 7
    elif row['Age'] >= 24 and row['Age'] < 26:
        age_value = 8
    elif row['Age'] >= 22 and row['Age'] < 24:
        age_value = 9
    elif row['Age'] <= 22:
        age_value = 10
    return round(((value_batting + value_bowling + age_value)/3),2)

Merged_Player_df['player_type'] = Merged_Player_df.apply(lambda row: player_type(row),axis=1)
Merged_Player_df['player_rating'] = Merged_Player_df.apply(lambda row: player_rating(row),axis=1)

Merged_Player_df = Merged_Player_df.loc[:,['Player', 'Runs', 'Wickets', 'Age', 'Batting Skill','Bowling Skill', 'Country', 'player_type', 'player_rating']]
max_val = Merged_Player_df['player_rating'].max()
min_val = Merged_Player_df['player_rating'].min()

values = Merged_Player_df['player_rating'].tolist()
scaled_ratings = [round(((((10.0-0.0)*(x-min_val))/(max_val-min_val))+0.0),2) for x in values]
Merged_Player_df['player_rating'] = scaled_ratings

def Player_result(row):
    if row['player_rating'] < 2.5:
        return 'Below Average'
    elif row['player_rating'] >= 2.5 and row['player_rating'] < 5.0:
        return 'Average buy'
    elif row['player_rating'] >= 5.0 and row['player_rating'] < 7.5:
        return 'Good Player'
    else:
        return 'Outstanding Player'


Merged_Player_df['player_result'] = Merged_Player_df.apply(lambda row: Player_result(row),axis=1)
print(Merged_Player_df)

##Model Building

## Prepare Train and Test Splits

X = Merged_Player_df.iloc[:, 1:4].values
Y = Merged_Player_df.iloc[:,9].values
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state = 40)

print('1. XGBClassifier')

model = XGBClassifier()

model.fit(X_train, Y_train)

#Make predictions for test data
y_pred1 = model.predict(X_test)


## Calculating Metrics

cm1 = confusion_matrix(Y_test, y_pred1)
print (cm1)
from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test, y_pred1)*100,"% Accuracy")

print('2. DecisionTreeClassifier')

classifier = DecisionTreeClassifier()

classifier = classifier.fit(X_train,Y_train)

#Make predictions for test data
y_pred2 = classifier.predict(X_test)

cm2 = confusion_matrix(Y_test, y_pred2)
print (cm2)
from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test, y_pred2)*100,"% Accuracy")

print('3. RandomForestClassifier')

#Create a Gaussian Classifier
rand_forest=RandomForestClassifier(n_estimators=100)

#Train the model using the training sets y_pred=clf.predict(X_test)
rand_forest = rand_forest.fit(X_train,Y_train)

y_pred3 = rand_forest.predict(X_test)

cm3 = confusion_matrix(Y_test, y_pred3)
print (cm3)
from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test, y_pred3)*100,"% Accuracy")
