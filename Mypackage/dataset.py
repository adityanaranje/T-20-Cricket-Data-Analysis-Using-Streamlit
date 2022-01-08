import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
import requests

@st.cache
def get_data():
    df1 = pd.read_csv('Datasets/Ball_by_ball_data.csv')
    df2 = pd.read_csv('Datasets/Match_data.csv')
    df3 = pd.read_csv('Datasets/Summary.csv')
    df4 = pd.read_csv('Datasets/city_df.csv')
    return df1, df2, df3, df4
    
@st.cache
def current_df():
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/t20i"
    req=requests.get(url)
    content = req.text

    soup = BeautifulSoup(content)

    first_data = soup.find('tr', class_='rankings-block__banner') 

    first_pos = first_data.find('td', class_="rankings-block__banner--pos")
    first_team = first_data.find('span',class_="u-hide-phablet")
    first_matches = first_data.find('td', class_="rankings-block__banner--matches")
    first_points = first_data.find('td', class_="rankings-block__banner--points")
    first_rating = first_data.find('td', class_="rankings-block__banner--rating u-text-right")


    positions = []
    teams = []
    matches = []
    points = []
    ratings = []

    for i in first_pos:
        positions.append(i)
    for i in first_team:
        teams.append(i)
    for i in first_matches:
        matches.append(i)
    for i in first_points:
        points.append(i)
    for i in first_rating:
        i = i.replace(" ", '')
        i = i.replace("\n",'')
        ratings.append(i)
        break
        
    all_pos = soup.find_all('td',class_="table-body__cell table-body__cell--position u-text-right")

    for i in all_pos:
        for d in i:
            positions.append(d)

    all_teams = soup.find_all('td', class_="table-body__cell rankings-table__team")
    for i in all_teams:
        x = i.find('span', class_="u-hide-phablet")
        for d in x:
            teams.append(d)
            
    all_matches = soup.find_all('td', class_="table-body__cell u-center-text")
    x = 1
    for i in all_matches:
        for d in i:
            if x ==1:
                matches.append(d)
            if x==2:
                points.append(d)
            x+=1
            if x>2:
                x =1
    all_ratings = soup.find_all('td', class_="table-body__cell u-text-right rating")

    for i in all_ratings:
        for d in i:
            ratings.append(d)

    current_standings = pd.DataFrame()
            
    current_standings['Position'] = positions
    current_standings['Team'] = teams
    current_standings['Matches'] = matches
    current_standings['Points'] = points
    current_standings['Ratings'] = ratings
    return current_standings