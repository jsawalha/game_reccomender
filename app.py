from pdb import post_mortem
import pickle
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests


#Import the pickle files we will need
df = pickle.load(open('./game_list.pkl','rb'))
similarity = pickle.load(open('./similarity.pkl','rb'))

#This function fetches the link of the image on the game page
def fetch_poster(game_id):
    #Get url from the selected game by the user
    url = "https://www.dekudeals.com/items/{}".format(game_id)
    data = requests.get(url)
    soup = BeautifulSoup(data.content, "html.parser")

    #find the link image from the game page, if we cant, replace it with a 'no image availble' image
    try:
        img_link = soup.find('img', {"width": "500", "height": "500", "alt": ""}).get('src')
    except:
        img_link = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Noimage.svg/347px-Noimage.svg.png'
    return img_link

#This function incorporates the top 5 reccomendations based on cosine similarity, but also factors in developer, genre, and meta_critic scores
def get_recommendations(title):
    """
    We are incorperating pandas, because I need to sort the top cosine similarity games in terms of developer, genre, and meta_critic scores
    """

    #using DF, get column with just titles
    titles = df['title']
    #Make indices
    indices = pd.Series(df.index, index=df['title'])
    
    #get index of our game, print similarity scores for that game, from 1-60
    idx = indices[title]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:100]
    game_indices = [i[0] for i in sim_scores]

    #Make a dataframe of those 60 top games
    games = df.iloc[game_indices][['title', 'Genre', 'Developer', 'Download size', 'meta_critic', 'meta_user']]

    #qualified is our final dataframe, sorted, for top reccomendations
    qualified = pd.DataFrame()

    #We need to find the developer, genre, and publisher of the target game
    if 'nan' in df['Developer'].iloc[idx]:
        target_dev = 'nan'
    else:
        target_dev = df['Developer'].iloc[idx]

    if 'nan' in df['Genre'].iloc[idx]:
        target_gen = 'nan'
    else:
        target_gen = df['Genre'].iloc[idx]

    if 'nan' in df['Publisher'].iloc[idx]:
        target_pub = 'nan'
    else:
        target_pub = df['Publisher'].iloc[idx]

    #Add developer rows to qualified
    if games[games['Developer'] == target_dev].empty:
        pass
    else:
        qualified = pd.concat([qualified, games[games['Developer'] == target_dev]], ignore_index=True)

    #Add genre rows to qualified
    if 'nan' in target_gen:
        pass
    else:
        try:
                qualified = pd.concat([qualified, games[(games['Genre'].str.contains(target_gen.split()[0].replace(',', ''))) & (games['Genre'].str.contains(target_gen.split()[1].replace(',', '')))]], ignore_index=True)
        except:
                qualified = pd.concat([qualified, games[(games['Genre'].str.contains(target_gen.split()[0].replace(',', '')))]], ignore_index=True)

    #Add meta critic scores to qualified

    #Gotta turn these columns into a int
    games['meta_user'] = games['meta_user'].astype(float).astype(int)
    games['meta_critic'] = games['meta_critic'].astype(float).astype(int)

    #Get all games that are above a 6 in meta critic, and sort them, highest to lowest
    if games[(games['meta_critic'] >= 60) & (games['meta_user'] >= 6)].empty:
        pass
    else:
        qualified = pd.concat([qualified, games[(games['meta_critic'] >= 60) & (games['meta_user'] >= 6)].sort_values(by = ['meta_critic'], ascending=False)], ignore_index=True)

    # qualified.sort_values(by=['Developer', 'Genre', 'meta_critic'], ascending= (False, False, True), inplace=True)


    #fetch posters for all 5 games

    #game poster is gonna involve all the links for that game
    game_posters = []


    #For the top 5 games, get the image links from their web pages
    for k in qualified['title'].head(5):
        game_posters.append(fetch_poster(k))
    
    game_names = qualified['title'].head(5)



    return game_names, game_posters


#Set background image
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://img.wallpapersafari.com/desktop/1920/1080/39/45/0glWAP.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
#Call background image
set_bg_hack_url()

st.header('Ultimate Game Recommender System')


game_list = df['title'].values
selected_game = st.selectbox(
    "Type or select a game from the dropdown",
    game_list
)

if st.button('Show Recommendation'):
    recommended_game_names, recommended_game_posters = get_recommendations(selected_game)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_game_names[0])
        st.image(recommended_game_posters[0])
    with col2:
        st.text(recommended_game_names[1])
        st.image(recommended_game_posters[1])

    with col3:
        st.text(recommended_game_names[2])
        st.image(recommended_game_posters[2])
    with col4:
        st.text(recommended_game_names[3])
        st.image(recommended_game_posters[3])
    with col5:
        st.text(recommended_game_names[4])
        st.image(recommended_game_posters[4])
