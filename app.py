import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
from Mypackage import dataset, helper
from PIL import Image
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('static/bgg.jpg')



img = Image.open('static/sideimage.jpg')


ball_df, match_df, summary, city_df = dataset.get_data()

st.sidebar.image(img)
st.sidebar.title("T20 Cricket Analysis From (2005-2021)")
st.sidebar.text("By Adity Naranje")

user_menu = st.sidebar.radio(
    'Select Option',
    ('Overview','Overall Analysis','Teamwise Analysis','Yearwise Analysis')
)


if user_menu=='Overview':
    st.title("Top Statistics")

    total_matches = ball_df['Match No'].nunique()
    total_teams = ball_df['Batting Team'].nunique()
    total_balls_bowled = len(ball_df)
    players = ball_df['Striker'].append(ball_df['Bowler'])
    total_players = players.nunique()

    total_fours = len(ball_df[ball_df['Boundry']==4])
    total_sixes = len(ball_df[ball_df['Boundry']==6])
    total_runs = ball_df['Total Runs'].sum()


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Matches")
        st.title(total_matches)
    with col2:
        st.header("Teams")
        st.title(total_teams)
    with col3:
        st.header("Players")
        st.title(total_players)
    with col4:
        st.header("Balls")
        st.title(total_balls_bowled)
        

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Fours")
        st.title(total_fours)
    with col2:
        st.header("Sixes")
        st.title(total_sixes)
    with col3:
        st.header("Runs")
        st.title(total_runs)

    
    data = match_df[['latitude','longitude']]
    data.dropna(inplace=True)
    st.title("Match Venues")
    st.map(data)

    try:
        df = dataset.current_df()
        df = df.set_index('Position')
        st.title("Current T-20 Standings")
        st.table(df)
    except:
        pass

if user_menu=='Overall Analysis':
    st.title("Team Summary")
    st.subheader("Ranked By Matches Played")
    st.dataframe(summary)

    st.title("Venue Summary")
    st.dataframe(city_df)


    matches_per_year_df = helper.data_per_year(ball_df, match_df, 'Match No')
    st.title("Total Matches Per Year")
    fig = px.line(matches_per_year_df, x = "Year", y = "Value", height=600, width=900, labels=dict(Value="Matches"))
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    teams_per_year_df = helper.data_per_year(ball_df, match_df, 'Batting Team')
    st.title("Number of Teams Playing Per Year")
    fig = px.line(teams_per_year_df, x = "Year", y = "Value", height=600, width=900, labels=dict(Value="Teams"))
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    maxscore_per_year_df = helper.maxscore_per_year(ball_df, match_df)
    st.title("Max Score Per Year")
    fig = px.line(maxscore_per_year_df, x = "Year", y = "Max_Score", height=600, width=900, labels=dict(Max_Score="Highest Score"))
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    boundry_per_year_df = helper.boundry_per_year(ball_df, match_df)
    st.title("Boundries Per Year")
    fig = px.line(boundry_per_year_df, x = "Year", y = ['Fours','Sixes'], height=600, width=900,labels=dict(value='Count', variable='Boundries'))
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)



if user_menu=='Teamwise Analysis':
    total_teams = ball_df['Batting Team'].unique()
    total_teams.sort()
    selected_team = st.sidebar.selectbox("Select a team",total_teams)

    total_teams = list(total_teams)
    total_teams.remove(selected_team)
    total_teams.insert(0, 'All')
    opponent_team = st.sidebar.selectbox("Select opponent team", total_teams)

    d1, d2, d3, d4, d5, d6, d7 = helper.team_summary(ball_df,match_df, selected_team, opponent_team)

    st.title(selected_team+" VS "+opponent_team)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Matches")
        st.title(d1)
    with col2:
        st.header("Players")
        st.title(d2)
    with col3:
        st.header("Win %")
        st.title(d3)
    with col4:
        st.header("Runs")
        st.title(d4)

    col1, col2, col3  = st.columns(3)
    with col1:
        st.header("Fours")
        st.title(d5)
    with col2:
        st.header("Sixes")
        st.title(d6)
    with col3:
        st.header("Highest Score")
        st.title(d7)


    df = helper.team_top_scorers(ball_df, selected_team, opponent_team)
    st.header("Most Runs Against "+opponent_team)
    fig = fig = px.bar(df, x = "Player", y = 'Runs',color='Player' ,height=600, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    df = helper.team_top_fours(ball_df, selected_team, opponent_team)
    st.header("Most Fours Against "+opponent_team)
    fig = fig = px.bar(df, x = "Player", y = 'Fours',color='Player' ,height=600, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    df = helper.team_top_sixes(ball_df, selected_team, opponent_team)
    st.header("Most Sixes Against "+opponent_team)
    fig = fig = px.bar(df, x = "Player", y = 'Sixes',color='Player' ,height=600, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    df = helper.team_most_balls(ball_df, selected_team, opponent_team)
    st.header("Most Balls Played Against "+opponent_team)
    fig = fig = px.bar(df, x = "Player", y = 'Balls Played',color='Player' ,height=600, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df, l = helper.best_strikerate(ball_df, selected_team, opponent_team)
    st.header("Best Strike Rate Against "+opponent_team+" min("+str(l)+" balls)")
    fig = px.bar(df, x ="Player" , y = "Strike Rate",color='Player' ,height=600, width=1000)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    if opponent_team!='All':
        temp_df = match_df[((match_df['Team1']==selected_team) & (match_df['Team2']==opponent_team)) | ((match_df['Team1']==opponent_team) & (match_df['Team2']==selected_team))]
    else:
        temp_df = match_df[(match_df['Team1']==selected_team) | (match_df['Team2']==selected_team)]
        temp_df['Winner'] = np.where(temp_df['Winner']==selected_team, selected_team,"Others")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(temp_df,x = 'Winner',color='Winner', height=350,width=370)
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.header("Win Comparision")
        st.plotly_chart(fig)

    with col2:
        df = temp_df
        df['Toss Winner'] = np.where(df['Toss Winner']==selected_team,selected_team,'Others')
        fig = px.histogram(df,x = 'Toss Winner',color='Toss Winner', height=350,width=370)
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.header("Toss Winner")
        st.plotly_chart(fig)


    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(temp_df,x = 'Winner',color='Won By', height=350,width=370)
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.header("Win Method")
        st.plotly_chart(fig)

    with col2:
        df = temp_df
        df['Toss Winner'] = np.where(df['Toss Winner']==selected_team,selected_team,'Others')
        fig = px.histogram(df,x = 'Toss Winner',color='Toss Decision', height=350,width=370)
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.header("Toss Decision")
        st.plotly_chart(fig)


    df = helper.best_strikerate_death(ball_df, selected_team, opponent_team)
    st.header("Best Strike Rate At Death Overs Against "+opponent_team)
    fig = px.bar(df, x ="Strike Rate" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df = helper.most_boundry_death(ball_df, selected_team,opponent_team)
    st.header("Most Boundaries At Death Overs Against "+opponent_team)
    fig = px.bar(df, x ="Boundry" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df = helper.most_runs_powerplay(ball_df, selected_team,opponent_team)
    st.header("Most Runs At Powerplay Against "+opponent_team)
    fig = px.bar(df, x ="Runs" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df = helper.most_boundry_powerplay(ball_df, selected_team,opponent_team)
    st.header("Most Boundaries At Powerplay Against "+opponent_team)
    fig = px.bar(df, x ="Boundry" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


if user_menu=='Yearwise Analysis':
    year_list = match_df['Year'].unique()
    year_list.sort()
    selected_year = st.sidebar.selectbox("Select a year", year_list)
    
    total_teams = ball_df['Batting Team'].unique()
    total_teams.sort()
    total_teams = list(total_teams)
    selected_team = st.sidebar.selectbox("Select a team",total_teams)

    new_ball_df = pd.merge(ball_df, match_df[['Match No','Year']], how="left", left_on="Match No", right_on="Match No")

    d1, d2, d3, d4, d5, d6, d7 = helper.yearwise_summary(new_ball_df,match_df,selected_year,selected_team)

    st.title(selected_team+" In "+str(selected_year))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Matches")
        st.title(d1)
    with col2:
        st.header("Players")
        st.title(d2)
    with col3:
        st.header("Win %")
        st.title(d3)
    with col4:
        st.header("Runs")
        st.title(d4)

    col1, col2, col3  = st.columns(3)
    with col1:
        st.header("Fours")
        st.title(d5)
    with col2:
        st.header("Sixes")
        st.title(d6)
    with col3:
        st.header("Highest Score")
        st.title(d7)

    total_score_per_year = helper.yearwise_totalscore(new_ball_df, selected_year, selected_team)
    st.title("Total Score VS Every Team In "+str(selected_year))
    fig = px.funnel(total_score_per_year, x = 'Bowling Team', y = 'Total Runs',color='Bowling Team', height=500, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    max_score_per_year = helper.yearwise_maxscore(new_ball_df, selected_year, selected_team)
    st.title("Max Score VS Every Team In "+str(selected_year))
    fig = px.funnel(max_score_per_year, x = 'Bowling Team', y = 'Score',color='Bowling Team', height=500, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    total_match_per_year = helper.yearwise_totalmatch(new_ball_df, selected_year, selected_team)
    st.title("Total Matches VS Every Team In "+str(selected_year))
    fig = px.funnel(total_match_per_year, x = 'Bowling Team', y = 'Match No',color='Bowling Team', height=500, width=900, labels={'Match No':'Matches'})
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    extra_score_per_year = helper.yearwise_extraruns(new_ball_df, selected_year, selected_team)
    st.title("Extra Runs Scored Per Match VS Every Team In "+str(selected_year))
    fig = px.funnel(extra_score_per_year, x = 'Bowling Team', y = 'Average Runs',color='Bowling Team', height=500, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    boundry_per_year = helper.yearwise_boundry(new_ball_df, selected_year, selected_team)
    st.title("Average Boundries VS Every Team In "+str(selected_year))
    fig = px.funnel(boundry_per_year, x = 'Bowling Team', y = 'Average Boundry',color='Bowling Team', height=500, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    dotballs_per_year = helper.yearwise_dotballs(new_ball_df, selected_year, selected_team)
    st.title("Average Dot Balls VS Every Team In "+str(selected_year))
    fig = px.funnel(dotballs_per_year, x = 'Bowling Team', y = 'Average Dot Balls',color='Bowling Team', height=500, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)



    average_score_per_year = helper.inning_avgscore_peryear(new_ball_df, selected_year, selected_team)
    st.title("Average Score Per Inning In "+str(selected_year))
    fig = px.histogram(average_score_per_year, x = 'Inning', y = 'Average Score',color='Inning', height=400, width=700)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)



    df = helper.best_strikerate_death_peryear(new_ball_df, selected_team, selected_year)
    st.header("Best Strike Rate At Death Overs In "+str(selected_year))
    fig = px.bar(df, x ="Strike Rate" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df = helper.most_boundry_death_peryear(new_ball_df, selected_team,selected_year)
    st.header("Most Boundaries At Death Overs In "+str(selected_year))
    fig = px.bar(df, x ="Boundry" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df = helper.most_runs_powerplay_peryear(new_ball_df, selected_team,selected_year)
    st.header("Most Runs At Powerplay In "+str(selected_year))
    fig = px.bar(df, x ="Runs" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    df = helper.most_boundry_powerplay_peryear(new_ball_df, selected_team,selected_year)
    st.header("Most Boundaries At Powerplay In "+str(selected_year))
    fig = px.bar(df, x ="Boundry" , y = "Player",color='Player' ,height=300, width=900)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)
