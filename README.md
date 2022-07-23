# Data-Management-ETL-Pipeline

The dataset is extracted from CSV files. The dataset is unclean initially. The data profiling has been performed on the columns, considering the quality dimensions like Completeness, Consistency, Validity, Accuracy. Followed by profiling the dataset has been cleaned considering all the dimensions mentioned above. ETL pipeline has been implemented by transforming the data and further staging it. Finally the clean data has been divided into various tables using Snowflake schema and loaded into Excel files.

Data Visualization and Machine Learning has been implemented and to analyse the data more thoroughly and get the answers to our questions. Here RandomForestClassifier has performed best for the classification, hence we can choose to perform the analysis.


![image](https://user-images.githubusercontent.com/45402305/180607598-60517b4b-9abe-4bed-90f8-5b23a7ea1720.png)

Smart Strategy Board!

![image](https://user-images.githubusercontent.com/45402305/180607716-efc8aa4d-d503-4ec7-8a32-4c3acc168d66.png)

Questions we want to answer from this data.

The basic idea of analyzing the IPL dataset is to get a fair idea about the players who have performed their best in all the seasons.

1.Which player performs Outstanding, Good, Average, Below Average ?
2.Who has won most man of the match awards ?
3.What is the likelihood of toss determining the win?
4.Which are the favorite venues of all time ?
5.What are the number of matches played each season ?

## Data Profiling

Data profiling is the process of examining the data available from an existing information source (e.g. a database or a file) and collecting statistics or informative summaries about that data.

Software used for data profiling : Python Environment

1. Raw_Ball_by_Ball file

Data Profiling on Raw_Ball_by_Ball, consisting of columns meeting the quality dimension measures.

![image](https://user-images.githubusercontent.com/45402305/180607786-7ae0bd14-7996-4566-994b-1a442f774bea.png)

2. Raw_Player_Match file

Data Profiling on Raw_Player_Match, consisting of columns meeting the quality dimension measures.

![image](https://user-images.githubusercontent.com/45402305/180607828-cf09f1e5-2938-4e56-aa31-6e561c94e127.png)

## ETL Pipeline

![image](https://user-images.githubusercontent.com/45402305/180608150-a2ef97a0-2a18-4749-8dbf-f58006f44759.png)


# Snow flake Schema

![image](https://user-images.githubusercontent.com/45402305/180608173-3d034b2d-a7e6-4186-897a-ba8cb9f2d5d4.png)

## Data Visualization

1. Who has won most man of the match awards 

![image](https://user-images.githubusercontent.com/45402305/180607917-b9cea33c-0413-45dc-bb6a-39aa9b2714de.png)

2. What is the likelihood of toss determining the win

![image](https://user-images.githubusercontent.com/45402305/180607925-f3e37db9-0448-48d1-a16e-520a111d3ef2.png)

3. Which are the favorite venues of all time

![image](https://user-images.githubusercontent.com/45402305/180607941-b3c47b9f-73de-4214-b2c5-adff7dd70b43.png)


4. What are the number of matches played each season

![image](https://user-images.githubusercontent.com/45402305/180607973-54b1031f-4678-434a-b2f7-3fd34a3d9ce4.png)

## Data Preparation for Analysis

A dataframe was created by combining the columns from various tables to create the data which will further be useful for creating a machine learning model and analyse which Player performs Below Average, Average, Good and Outstanding. These are the four categories the players are classified.

1.Below Average
2.Average
3.Good
4.Outstanding

## Machine Learning Algorithm

3 Machine Learning algorithm are implemented for analyzing the performance of each player. Mentioned below are the three model with their corresponding accuracy.

1.XGBClassifier  (Accuracy – 92.75%) 

2.DecisionTreeClassifier   (Accuracy - 90.57 %)

3.RandomForestClassifier  (Accuracy – 92.80%)

As we can see that RandomForestClassifier is giving better accuracy as compared to other classifiers. Hence we can choose the RandomForestClassifier for classifying the player 















