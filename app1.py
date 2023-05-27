import pandas as pd
import numpy as np
import plotly.express as px
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


user_menu = st.sidebar.radio(
    'Select Option',
    ('Overview','Player Stats','Players Comparision','Overall Analysis','Teamwise Analysis','Yearwise Analysis')
)


if user_menu=='Overview':
    st.title("Top Statistics")

    total_matches = ball_df['Match No'].nunique()
    total_teams = ball_df['Batting Team'].nunique()
    total_balls_bowled = len(ball_df)
    x = ball_df["Striker"]
    players = x.append(ball_df['Bowler'])
    total_players = players.nunique()

    total_fours = len(ball_df[ball_df['Boundry']==4])
    total_sixes = len(ball_df[ball_df['Boundry']==6])
    total_runs = ball_df['Total Runs'].sum()


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Matches")
        st.subheader(total_matches)
    with col2:
        st.header("Teams")
        st.subheader(total_teams)
    with col3:
        st.header("Players")
        st.subheader(total_players)
    with col4:
        st.header("Balls")
        st.subheader(total_balls_bowled)
        

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Fours")
        st.subheader(total_fours)
    with col2:
        st.header("Sixes")
        st.subheader(total_sixes)
    with col3:
        st.header("Runs")
        st.subheader(total_runs)

    
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
    summary = summary.style.background_gradient(cmap="Blues")
    st.dataframe(summary)

    st.title("Venue Summary")
    city_df = city_df.style.background_gradient(cmap="Blues")
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


    if d1==0:
        st.info(selected_team + " not played any match in year "+str(selected_year))
    else:
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
    
    
if user_menu=='Player Stats':
    players = sorted(list(ball_df['Striker'].unique()))
    
    selected_player = st.sidebar.selectbox("Player", players)
    
    st.header(f"{selected_player} Stats")
    
    dff = ball_df[ball_df['Striker']==selected_player][["Striker","Batter Runs","Batting Team","Inning","Boundry"]]
    batting_team = str(dff['Batting Team'].unique()[0])
    dff1 = ball_df[ball_df['Batting Team']==batting_team]
    total_batter_runs = dff.groupby(by="Striker").sum()["Batter Runs"]

    total_team_runs = sum(dff1['Batter Runs'])

    total_batter_runs = total_batter_runs[0]

    run_per = int(np.ceil((total_batter_runs/total_team_runs)*100))
    
    balls_faced = len(dff)
    fours = len(dff[dff["Boundry"]==4])
    sixes = len(dff[dff["Boundry"]==6])

    strike_rate = round((total_batter_runs/balls_faced)*100, 2)
    
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Team")
        st.subheader(batting_team)
    with col2:
        st.header("Runs")
        st.subheader(total_batter_runs)
    with col3:
        st.header("Runs %")
        st.subheader(run_per)
    with col4:
        st.header("Sixes")
        st.subheader(sixes)

        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Fours")
        st.subheader(fours)
        
    with col2:
        st.header("Balls Faced")
        st.subheader(balls_faced)
        
    with col3:
        st.header("Strike Rate")
        st.subheader(strike_rate)
    
    
    # Stats against bowlers
    
    st.title("Stats Against Bolwers")
    
    sorting = st.selectbox("Sorting By", ["Strike Rate","Batter Runs", "Ball", "Fours", "Sixes"])
    
    asc = st.radio("Sort", ["Descending","Ascending"])
    
    if asc=="Ascending":
        asc = True
    else:
        asc = False
        
    df = ball_df[ball_df["Striker"]==selected_player]
    
    d1 = df.groupby("Bowler")["Batter Runs"].sum().reset_index()
    d2 = df.groupby("Bowler")["Ball"].count().reset_index()
    df_4 = df[df["Boundry"]==4]
    df_6 = df[df["Boundry"]==6]
    
    d3 = df_4.groupby("Bowler")["Boundry"].count().reset_index()
    d4 = df_6.groupby("Bowler")["Boundry"].count().reset_index()
    d3 = d3.rename(columns={"Boundry":"Fours"})
    d4 = d4.rename(columns={"Boundry":"Sixes"})
    
    data1 = d1.merge(d2, on="Bowler", how="outer")
    data2 = d3.merge(d4, on="Bowler", how="outer")
    data = data1.merge(data2, on="Bowler", how="outer")
    
    data["Strike Rate"] = np.round((data["Batter Runs"]/data["Ball"])*100, 2)
    data = data.sort_values(by=sorting, ascending=asc).reset_index()

    data.fillna(int(0), inplace=True)
    data.drop(columns=["index"], inplace=True)
    data["Fours"] = data["Fours"].astype("int")
    data["Sixes"] = data["Sixes"].astype("int")

    data = data.style.background_gradient(cmap="Blues")
    
    st.dataframe(data)
    
    
    # Stats Agains Teams
    st.title("Stats Against Teams")
        
    df = ball_df[ball_df["Striker"]==selected_player]
    
    d1 = df.groupby("Bowling Team")["Batter Runs"].sum().reset_index()
    d2 = df.groupby("Bowling Team")["Ball"].count().reset_index()
    df_4 = df[df["Boundry"]==4]
    df_6 = df[df["Boundry"]==6]
    
    d3 = df_4.groupby("Bowling Team")["Boundry"].count().reset_index()
    d4 = df_6.groupby("Bowling Team")["Boundry"].count().reset_index()
    d3 = d3.rename(columns={"Boundry":"Fours"})
    d4 = d4.rename(columns={"Boundry":"Sixes"})
    
    data1 = d1.merge(d2, on="Bowling Team", how="outer")
    data2 = d3.merge(d4, on="Bowling Team", how="outer")
    data = data1.merge(data2, on="Bowling Team", how="outer")
    
    data["Strike Rate"] = np.round((data["Batter Runs"]/data["Ball"])*100, 2)
    data = data.sort_values(by=sorting, ascending=asc).reset_index()

    data.fillna(int(0), inplace=True)
    data.drop(columns=["index"], inplace=True)
    data["Fours"] = data["Fours"].astype("int")
    data["Sixes"] = data["Sixes"].astype("int")

    data = data.rename(columns={"Bowling Team":"Team", "Batter Runs":"Runs"})
    data = data.style.background_gradient(cmap="winter")
    
    st.dataframe(data)
    
    
    
if user_menu=='Players Comparision':
    
    players1 = sorted(list(ball_df['Striker'].unique()))
    selected_player1 = st.sidebar.selectbox("Player1", players1)
    
    players2 = list(players1)
    players2.remove(selected_player1)
    selected_player2 = st.sidebar.selectbox("Player2", players2)
    
        
    # Player1
    dff = ball_df[ball_df['Striker']==selected_player1][["Striker","Batter Runs","Batting Team","Inning","Boundry"]]
    batting_team1 = str(dff['Batting Team'].unique()[0])
    dff1 = ball_df[ball_df['Batting Team']==batting_team1]
    total_batter_runs1 = dff.groupby(by="Striker").sum()["Batter Runs"]
    total_team_runs1 = sum(dff1['Batter Runs'])
    total_batter_runs1 = total_batter_runs1[0]
    run_per1 = int(np.ceil((total_batter_runs1/total_team_runs1)*100))
    balls_faced1 = len(dff)
    fours1 = len(dff[dff["Boundry"]==4])
    sixes1 = len(dff[dff["Boundry"]==6])
    strike_rate1 = round((total_batter_runs1/balls_faced1)*100, 2)

    dff = ball_df[ball_df['Striker']==selected_player2][["Striker","Batter Runs","Batting Team","Inning","Boundry"]]
    batting_team2 = str(dff['Batting Team'].unique()[0])
    dff2 = ball_df[ball_df['Batting Team']==batting_team2]
    total_batter_runs2 = dff.groupby(by="Striker").sum()["Batter Runs"]
    total_team_runs2 = sum(dff2['Batter Runs'])
    total_batter_runs2 = total_batter_runs2[0]
    run_per2 = int(np.ceil((total_batter_runs2/total_team_runs2)*100))
    balls_faced2 = len(dff)
    fours2 = len(dff[dff["Boundry"]==4])
    sixes2 = len(dff[dff["Boundry"]==6])
    strike_rate2 = round((total_batter_runs2/balls_faced2)*100, 2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header(f"{selected_player1}")
    with col2:
        st.header("    VS")
    with col3:
        st.header(f"{selected_player2}")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(f"({batting_team1})")
    with col2:
        st.header("")
    with col3:
        st.subheader(f"({batting_team2})")
        

    data = pd.DataFrame()

    data["Player"] = [selected_player1, selected_player2]
    data["Team"] = [batting_team1, batting_team2]
    data["Runs"] = [total_batter_runs1, total_batter_runs2]
    data["Run %"] = [run_per1, run_per2]
    data["Balls"] = [balls_faced1, balls_faced2]
    data["Sixes"] = [sixes1, sixes2]
    data["Fours"] = [fours1, fours2]
    data["Strike Rate"] = [strike_rate1, strike_rate2]
    
    # Most Runs
    st.header("Runs")
    fig = px.pie(data, values="Runs", names = "Player" , height=300, width=600)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
    st.plotly_chart(fig)
    
    # Run %
    st.header("Run % for Team")
    fig = px.pie(data, values="Run %", names = "Player" , height=300, width=600)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
    st.plotly_chart(fig)
    
    # Balls Played
    st.header("Balls Played")
    fig = px.pie(data, values="Balls", names = "Player" , height=300, width=600)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
    st.plotly_chart(fig)
    
    
    # Sixes
    st.header("Sixes")
    fig = px.bar(data, x= "Player", y = "Sixes", color="Player", height=400, width=600, text="Sixes")
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    st.plotly_chart(fig)
    
    # Fours
    st.header("Fours")
    fig = px.bar(data, x= "Player", y = "Fours", color="Player", height=400, width=600, text="Fours")
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    st.plotly_chart(fig)
    
    # Strike Rate
    st.header("Strike Rate")
    fig = px.bar(data, x= "Player", y = "Strike Rate", color="Player", height=400, width=600, text="Strike Rate")
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_traces(texttemplate='%{text:.5s}', textposition='inside')
    st.plotly_chart(fig)
