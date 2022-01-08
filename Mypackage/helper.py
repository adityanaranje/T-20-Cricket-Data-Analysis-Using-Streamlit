import pandas as pd
import numpy as np

def data_per_year(df1, df2, col):
    years_df = pd.merge(df1[['Match No','Batting Team','Total Runs','Score','Boundry']],df2[['Match No','Year']], 
                   how='left', left_on='Match No', right_on='Match No')

    years_list = years_df['Year'].unique()
    years_list.sort()

    year = []
    value = []

    for y in years_list:
        year.append(y)
        data = years_df[years_df['Year']==y][col].nunique()
        value.append(data)
    temp_df = pd.DataFrame()
    temp_df['Year'] = year
    temp_df['Value'] = value

    return temp_df

def maxscore_per_year(df1, df2):
    years_df = pd.merge(df1[['Match No','Batting Team','Total Runs','Score','Boundry']],df2[['Match No','Year']], 
                   how='left', left_on='Match No', right_on='Match No')
    years_list = years_df['Year'].unique()
    years_list.sort()
    year = []
    value = []

    for y in years_list:
        year.append(y)
        data = years_df[years_df['Year']==y]['Score'].max()
        value.append(data)
    temp_df = pd.DataFrame()
    temp_df['Year'] = year
    temp_df['Max_Score'] = value

    return temp_df

def boundry_per_year(df1, df2):
    years_df = pd.merge(df1[['Match No','Batting Team','Total Runs','Score','Boundry']],df2[['Match No','Year']], 
                   how='left', left_on='Match No', right_on='Match No')
    years_list = years_df['Year'].unique()
    years_list.sort()
    year = []
    fours = []
    sixes = []

    for y in years_list:
        year.append(y)
        data1 = years_df[(years_df['Year']==y) & (years_df['Boundry']==4)]['Boundry'].count()
        fours.append(data1)
        data2 = years_df[(years_df['Year']==y) & (years_df['Boundry']==6)]['Boundry'].count()
        sixes.append(data2)
    temp_df = pd.DataFrame()
    temp_df['Year'] = year
    temp_df['Fours'] = fours
    temp_df['Sixes'] = sixes
    return temp_df


def team_summary(ball_df,match_df, selected_team, opponent_team):
    if opponent_team=='All':
        temp_df = ball_df[ball_df['Batting Team']==selected_team]
    else:
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Bowling Team']==opponent_team)]
    total_matches = temp_df['Match No'].nunique()
    if total_matches>0:
        players = temp_df['Striker'].append(temp_df['Bowler'])
        total_players = players.nunique()

        if opponent_team=='All':
            df = match_df[(match_df['Team1']==selected_team) | (match_df['Team2']==opponent_team)]
        else:
            df = match_df[((match_df['Team1']==selected_team) & (match_df['Team2']==opponent_team)) | ((match_df['Team1']==opponent_team) & (match_df['Team2']==selected_team))]
        win_per = round((df[df['Winner']==selected_team]['Winner'].count()/df['Winner'].count())*100,2)

        runs_scored = temp_df['Total Runs'].sum()
        total_fours = len(temp_df[temp_df['Boundry']==4])
        total_sixes = len(temp_df[temp_df['Boundry']==6])
        highest_score = temp_df['Score'].max()
    else:
        total_players,win_per,runs_scored, total_fours, total_sixes, highest_score = 0,0,0,0,0,0
    return total_matches, total_players,win_per,runs_scored, total_fours, total_sixes, highest_score


def team_top_scorers(df, selected_team, opponent_team):
    if opponent_team=='All':
        temp_df = df[df['Batting Team']==selected_team]
    else:
        temp_df = df[(df['Batting Team']==selected_team) & (df['Bowling Team']==opponent_team)]

    df = temp_df[['Striker','Batter Runs']].groupby(by='Striker')['Batter Runs'].sum().reset_index().sort_values('Batter Runs', ascending=False)
    df = df.reset_index()
    df = df.rename(columns={'Striker':'Player','Batter Runs':'Runs'})
    df = df.drop(columns=['index']).head(10)

    return df


def team_top_fours(df, selected_team, opponent_team):
    if opponent_team=='All':
        temp_df = df[df['Batting Team']==selected_team]
    else:
        temp_df = df[(df['Batting Team']==selected_team) & (df['Bowling Team']==opponent_team)]

    df = temp_df[temp_df['Boundry']==4]
    df = df[['Striker','Boundry']].groupby(by='Striker')['Boundry'].count().reset_index().sort_values('Boundry', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player','Boundry':'Fours'})
    df = df.drop(columns=['index']).head(10)
    return df


def team_top_sixes(df, selected_team, opponent_team):
    if opponent_team=='All':
        temp_df = df[df['Batting Team']==selected_team]
    else:
        temp_df = df[(df['Batting Team']==selected_team) & (df['Bowling Team']==opponent_team)]

    df = temp_df[temp_df['Boundry']==6]
    df = df[['Striker','Boundry']].groupby(by='Striker')['Boundry'].count().reset_index().sort_values('Boundry', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player','Boundry':'Sixes'})
    df = df.drop(columns=['index']).head(10)
    return df

def team_most_balls(df, selected_team, opponent_team):
    if opponent_team=='All':
        temp_df = df[df['Batting Team']==selected_team]
    else:
        temp_df = df[(df['Batting Team']==selected_team) & (df['Bowling Team']==opponent_team)]

    df = temp_df[['Striker','Ball']].groupby(by='Striker')['Ball'].count().reset_index().sort_values('Ball', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player','Ball':'Balls Played'})
    df = df.drop(columns=['index']).head(10)
    return df


def best_strikerate(df, selected_team, opponent_team):
    if opponent_team=='All':
        temp_df = df[df['Batting Team']==selected_team]
    else:
        temp_df = df[(df['Batting Team']==selected_team) & (df['Bowling Team']==opponent_team)]

    df1 = temp_df[['Striker','Ball']].groupby(by='Striker')['Ball'].count().reset_index()
    df1 = df1.rename(columns={'Striker':'Player','Ball':'Balls Played'})

    df2 = temp_df[['Striker','Batter Runs']].groupby(by='Striker')['Batter Runs'].sum().reset_index()
    df2 = df2.rename(columns={'Striker':'Player','Batter Runs':'Runs'})

    df = pd.merge(df1, df2, how='left', left_on='Player', right_on='Player')
    df['Strike Rate'] = round((df['Runs']/df['Balls Played'])*100, 3)
    if len(df[df['Balls Played']>=50])>=20:
        x = 150
    elif len(df[(df['Balls Played']>=30) & (df['Balls Played']<50)])>=15:
        x = 80
    else:
        x = 20
    df = df[df['Balls Played']>=x]
    df = df[['Player', 'Strike Rate']].sort_values(by='Strike Rate', ascending=False)
    return df, x


def best_strikerate_death(ball_df, selected_team, opponent_team):
    if opponent_team=="All":
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']>=16)]
    else:
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']>=16) & (ball_df['Bowling Team']==opponent_team)]
    df1 = temp_df[['Striker','Ball']].groupby(by='Striker')['Ball'].count().reset_index()
    df1 = df1.rename(columns={'Striker':'Player','Ball':'Balls Played'})

    df2 = temp_df[['Striker','Batter Runs']].groupby(by='Striker')['Batter Runs'].sum().reset_index()
    df2 = df2.rename(columns={'Striker':'Player','Batter Runs':'Runs'})
    df = pd.merge(df1, df2, how='left', left_on='Player', right_on='Player')
    df['Strike Rate'] = round((df['Runs']/df['Balls Played'])*100, 3)
    if len(df[df['Balls Played']>=30])>=3:
        df = df[df['Balls Played']>=30]
    df = df[['Player', 'Strike Rate']].sort_values(by='Strike Rate', ascending=False)

    return df.head(5)


def most_boundry_death(ball_df, selected_team, opponent_team):
    if opponent_team=="All":
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']>=16)]
    else:
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']>=16) & (ball_df['Bowling Team']==opponent_team)]
    df = temp_df[(temp_df['Boundry']==4) | (temp_df['Boundry']==6)]
    df = df[['Striker','Boundry']].groupby(by='Striker')['Boundry'].count().reset_index().sort_values('Boundry', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player'})
    df = df.drop(columns=['index'])
    return df.head(5)

def most_runs_powerplay(ball_df, selected_team, opponent_team):
    if opponent_team=="All":
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']<6)]
    else:
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']<6) & (ball_df['Bowling Team']==opponent_team)]

    df = temp_df[['Striker','Batter Runs']].groupby(by='Striker')['Batter Runs'].sum().reset_index().sort_values('Batter Runs', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player', 'Batter Runs':'Runs'})
    df = df.drop(columns=['index'])
    return df.head(5)


def most_boundry_powerplay(ball_df, selected_team, opponent_team):
    if opponent_team=="All":
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']<6)]
    else:
        temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']<6) & (ball_df['Bowling Team']==opponent_team)]

    df = temp_df[(temp_df['Boundry']==4) | (temp_df['Boundry']==6)]
    df = df[['Striker','Boundry']].groupby(by='Striker')['Boundry'].count().reset_index().sort_values('Boundry', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player'})
    df = df.drop(columns=['index'])
    return df.head(5)


def yearwise_summary(new_ball_df, match_df, selected_year, selected_team):
    temp_df1 = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]
    temp_df2 = match_df[(match_df['Year']==selected_year) & ((match_df['Team1']==selected_team) | (match_df['Team2']==selected_team))]

    total_matches = temp_df1['Match No'].nunique()
    if total_matches>0:
        players = temp_df1['Striker'].append(temp_df1['Bowler'])
        total_players = players.nunique()
        
        win_per = round((temp_df2[temp_df2['Winner']==selected_team]['Winner'].count()/temp_df2['Winner'].count())*100,2)

        runs_scored = temp_df1['Total Runs'].sum()
        total_fours = len(temp_df1[temp_df1['Boundry']==4])
        total_sixes = len(temp_df1[temp_df1['Boundry']==6])
        highest_score = temp_df1['Score'].max()
    else:
        total_players,win_per,runs_scored, total_fours, total_sixes, highest_score = 0,0,0,0,0,0

    return total_matches, total_players,win_per,runs_scored, total_fours, total_sixes, highest_score 


def yearwise_totalscore(new_ball_df, selected_year, selected_team):
    temp_df1 = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]
    temp_df1 = temp_df1.groupby('Bowling Team')['Total Runs'].sum().reset_index().sort_values(by='Total Runs')

    return temp_df1

def yearwise_maxscore(new_ball_df, selected_year, selected_team):
    temp_df1 = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]
    temp_df1 = temp_df1.groupby('Bowling Team')['Score'].max().reset_index().sort_values(by='Score')

    return temp_df1

def yearwise_totalmatch(new_ball_df, selected_year, selected_team):
    temp_df1 = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]
    temp_df1 = temp_df1.drop_duplicates(['Bowling Team','Match No'])
    temp_df1 = temp_df1.groupby('Bowling Team')['Match No'].count().reset_index().sort_values(by='Match No')

    return temp_df1

def yearwise_extraruns(new_ball_df, selected_year, selected_team):
    temp_df = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]

    temp_df1 = temp_df.drop_duplicates(['Bowling Team','Match No'])
    temp_df1 = temp_df1.groupby('Bowling Team')['Match No'].count().reset_index().sort_values(by='Match No')

    
    temp_df2 = temp_df.groupby('Bowling Team')['Extra Runs'].sum().reset_index().sort_values(by='Extra Runs')
    temp_df = pd.merge(temp_df1, temp_df2, how='left', left_on='Bowling Team', right_on='Bowling Team')
    temp_df['Average Runs'] = (temp_df['Extra Runs']/temp_df['Match No']).astype('int')
    temp_df = temp_df.sort_values(by='Average Runs')
    return temp_df


def yearwise_boundry(new_ball_df, selected_year, selected_team):
    temp_df = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]

    temp_df1 = temp_df.drop_duplicates(['Bowling Team','Match No'])
    temp_df1 = temp_df1.groupby('Bowling Team')['Match No'].count().reset_index().sort_values(by='Match No')

    temp_df2 = temp_df[temp_df['Boundry']>=4]
    temp_df2 = temp_df2.groupby('Bowling Team')['Boundry'].count().reset_index().sort_values(by='Boundry')
    temp_df = pd.merge(temp_df1, temp_df2, how='left', left_on='Bowling Team', right_on='Bowling Team')
    temp_df['Average Boundry'] = (temp_df['Boundry']/temp_df['Match No']).astype('int')
    temp_df = temp_df.sort_values(by='Average Boundry')
    return temp_df


def yearwise_dotballs(new_ball_df, selected_year, selected_team):
    temp_df = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]

    temp_df1 = temp_df.drop_duplicates(['Bowling Team','Match No'])
    temp_df1 = temp_df1.groupby('Bowling Team')['Match No'].count().reset_index().sort_values(by='Match No')

    temp_df2 = temp_df[temp_df['Total Runs']==0]
    temp_df2 = temp_df2.groupby('Bowling Team')['Total Runs'].count().reset_index().sort_values(by='Total Runs')
    temp_df = pd.merge(temp_df1, temp_df2, how='left', left_on='Bowling Team', right_on='Bowling Team')
    temp_df['Average Dot Balls'] = (temp_df['Total Runs']/temp_df['Match No']).astype('int')
    temp_df = temp_df.sort_values(by='Average Dot Balls')
    return temp_df


def inning_avgscore_peryear(new_ball_df,selected_year, selected_team):
    temp_df1 = new_ball_df[(new_ball_df['Year']==selected_year) & (new_ball_df['Batting Team']==selected_team)]
    df = temp_df1.groupby("Inning")['Total Runs'].mean()
    balls1 = (temp_df1[temp_df1['Inning']=='First']['Ball'].count())/(temp_df1[temp_df1['Inning']=='First']['Match No'].nunique())
    balls2 = (temp_df1[temp_df1['Inning']=='Second']['Ball'].count())/(temp_df1[temp_df1['Inning']=='Second']['Match No'].nunique())

    if (temp_df1[temp_df1['Inning']=='First']['Match No'].nunique())==0:
        balls1 = 0
    if (temp_df1[temp_df1['Inning']=='Second']['Match No'].nunique())==0:
        balls2=0
    temp_df = pd.DataFrame()
    temp_df['Inning'] = []
    temp_df['Average Score'] = []

    if balls1==0:
        score1 = 0
    else:
        score1 = int(df['First']*balls1)
        
    if balls2==0:
        score2 = 0
    else:
        score2 = int(df['Second']*balls2)
    
    temp_df['Inning'] = ['First Inning', 'Second Inning']
    temp_df['Average Score'] = [score1, score2]
    return temp_df


def best_strikerate_death_peryear(ball_df, selected_team, selected_year):
    temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']>=16) & (ball_df['Year']==selected_year)]
    df1 = temp_df[['Striker','Ball']].groupby(by='Striker')['Ball'].count().reset_index()
    df1 = df1.rename(columns={'Striker':'Player','Ball':'Balls Played'})

    df2 = temp_df[['Striker','Batter Runs']].groupby(by='Striker')['Batter Runs'].sum().reset_index()
    df2 = df2.rename(columns={'Striker':'Player','Batter Runs':'Runs'})
    df = pd.merge(df1, df2, how='left', left_on='Player', right_on='Player')
    df['Strike Rate'] = round((df['Runs']/df['Balls Played'])*100, 3)
    if len(df[df['Balls Played']>=30])>=3:
        df = df[df['Balls Played']>=30]
    df = df[['Player', 'Strike Rate']].sort_values(by='Strike Rate', ascending=False)

    return df.head(3)


def most_boundry_death_peryear(ball_df, selected_team, selected_year):
    temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']>=16) & (ball_df['Year']==selected_year)]
    df = temp_df[(temp_df['Boundry']==4) | (temp_df['Boundry']==6)]
    df = df[['Striker','Boundry']].groupby(by='Striker')['Boundry'].count().reset_index().sort_values('Boundry', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player'})
    df = df.drop(columns=['index'])
    return df.head(3)

def most_runs_powerplay_peryear(ball_df, selected_team, selected_year):
    temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']<6) & (ball_df['Year']==selected_year)]

    df = temp_df[['Striker','Batter Runs']].groupby(by='Striker')['Batter Runs'].sum().reset_index().sort_values('Batter Runs', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player', 'Batter Runs':'Runs'})
    df = df.drop(columns=['index'])
    return df.head(3)


def most_boundry_powerplay_peryear(ball_df, selected_team, selected_year):
    temp_df = ball_df[(ball_df['Batting Team']==selected_team) & (ball_df['Over']<6) & (ball_df['Year']==selected_year)]

    df = temp_df[(temp_df['Boundry']==4) | (temp_df['Boundry']==6)]
    df = df[['Striker','Boundry']].groupby(by='Striker')['Boundry'].count().reset_index().sort_values('Boundry', ascending=False)
    df.reset_index(inplace=True)
    df = df.rename(columns={'Striker':'Player'})
    df = df.drop(columns=['index'])
    return df.head(3)