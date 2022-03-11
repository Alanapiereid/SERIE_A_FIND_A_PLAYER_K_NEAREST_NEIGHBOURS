from numpy.core.numeric import NaN
import pandas as pd
import math
from scipy.spatial import distance
import streamlit as st
# get 'players.csv' and 'appearances.csv' from Kaggle:
# https://www.kaggle.com/davidcariboo/player-scores

# DATA WRANGLING #
df = pd.read_csv('players.csv', encoding='utf-8')
# I manually made a list of Serie A club IDs
club_IDs = list(df['ID'][:20].astype(int))
club_IDs = [str(x) for x in club_IDs]
club_names = list(df['Club'][:20])
dict = {club_names[i]: club_IDs[i] for i in range(len(club_names))}
# Here's a dictionary of clubs + IDs
#{'Inter': '46', 'Napoli': '6195', 'Juve': '506', 'AC Milan': '5', 'Torino': '416', 'Sassuolo': '6574', 'Salernitana': '380', 'Roma': '12', 'Lazio': '398', 'Atalanta': '800', 'Cagliari': '1390', 'Empoli': '749', 'Udinese': '410', 'Sampdoria': '1038', 'Venezia': '607', 'Spezia': '3522', 'Genoa': '252', 'Verona': '276', 'Fiorentina': '430', 'Bologna': '1025'}
df = df[df['current_club_id'].isin(club_IDs)]
df = df.drop(columns=['market_value_in_gbp', 'url', 'Club', 'ID'])
player_IDs = df['player_id']
number_of_players = len(player_IDs)
# 1645 SERIE A players (includes youth teams)
#############################################################################################
df2 = pd.read_csv('appearances.csv', encoding='utf-8')
# just get Serie A players, so players with Serie A player IDs
df_ = df2[(df2['player_id'].isin(player_IDs)) & (df2['competition_id'] == 'IT1')]
df_ = df_.groupby('player_id').agg({'goals' : 'mean', 'assists' : 'mean', 'minutes_played' : 'mean', 'yellow_cards' : 'mean', 'red_cards' : 'mean'})
df = df.join(df_, on='player_id')

# NORMALIZATION #
numeric_columns = ['height_in_cm', 'highest_market_value_in_gbp', 'goals', 'assists', 'yellow_cards', 'red_cards']
normalize = df[numeric_columns]
normalized = (normalize - normalize.mean()) / normalize.std()
normalized.fillna(0, inplace=True)


import base64

main_bg = "flag2.png"
main_bg_ext = "png"



st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}

    </style>
    """,
    unsafe_allow_html=True
)


st.title("Find a Similar Serie A Player")
st.text("By Alan Reid | https://github.com/Alanapiereid")
text = st.text_input('Enter the name of a Serie A player')

trigger = st.button('Get Similar Player ')

if trigger:
    player_normalized = normalized[df["pretty_name"] == text]
    euc_distances = normalized.apply(lambda row: distance.euclidean(row, player_normalized), axis=1)
    distance_df = pd.DataFrame(data={"dist": euc_distances, "idx": euc_distances.index})
    distance_df.sort_values("dist", inplace=True)
    second_smallest = distance_df.iloc[1]["idx"]
    most_similar = df.loc[int(second_smallest)]["pretty_name"]
    st.text(most_similar)
    st.text(df[df["pretty_name"] == most_similar])






