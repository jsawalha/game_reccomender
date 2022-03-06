import numpy as np
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('./preprocessing/results_scraping.csv')

#Remove all rows with a non-description
df = df[pd.notnull(df['Description'])]

#drop last 2 columns
df.drop(['Demo Available', 'Releases', 'Release date'], axis=1, inplace=True)

#Removing non-english descriptions in the rows
df = df[df['Languages'].str.contains("English").fillna(True)]


#Fix released date
def split_date(text):
    if text is not 'nan':
        try:
            return re.findall(r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}", text)[0]
        except:
            pass

df['Released'] = df['Released'].apply(split_date)

#maybe we convert this to day time year

#Num of players
def split_players(text):
    if '-' in text:
        try:
            return re.findall(r"(?:\d\s*-\s*\d)+|\s{2,}", text)[-1]
        except:
            pass
    elif '-' not in text:
        try:
            return text.split(': ')[1]
        except:
            pass

df['Number of players'] = df['Number of players'].astype(str).apply(split_players)

#lower case for games
# def lower_case(text):
#     text = text.lower()
#     return text

# df['Name'] = df['Name'].apply(lower_case)

#How long to beat
def game_length(text):
    if ':' in text:
        try:
            return re.findall(r'\d+', text)[0]
        except:
            pass

df['How Long To Beat'] = df['How Long To Beat'].astype(str).apply(game_length)


#Download size
def convert_size(text):
    if "GB" in text:
        try:
            return pd.to_numeric(text.replace('GB', '').strip())
        except:
            pass
    elif "MB" in text:
        try:
            return pd.to_numeric(text.replace('MB', '').strip()) / 1000
        except:
            pass
    elif 'NaN' in text:
        pass

df['Download size'] = df['Download size'].astype(str).apply(convert_size)




#meta critic, split into critic and user score
df = df.join(df['Metacritic'].str.split(' ', 1, expand=True).rename(columns={0:'meta_critic', 1:'meta_user'}))

#drop column for meta critic
df.drop('Metacritic', axis=1, inplace=True)

#fill Nan's with -1's
df['meta_critic'] = df['meta_critic'].fillna(-1)
df['meta_user'] = df['meta_user'].fillna(-1)

#Convert all TBD into 0's
df['meta_critic'].replace('tbd', 0, inplace=True)
df['meta_user'].replace('tbd', 0, inplace=True)

#convert to int
df['meta_critic'] = df['meta_critic'].astype(int)
df['meta_user'] = df['meta_user'].astype(float)

#Meta lists
meta_user_idx = df[df['meta_user'] == 0]['meta_user'].index.tolist()
meta_critic_idx = df[df['meta_critic'] == 0]['meta_critic'].index.tolist()

#Converting meta critic scores that are tbd by using the meta USER scores

for k in meta_critic_idx:
    if df['meta_user'][k] != 0:
        df['meta_critic'][k] = df['meta_user'][k] * 10
    elif df['meta_user'][k] == -1:
        pass

for k in meta_user_idx:
    if df['meta_critic'][k] != 0:
        df['meta_user'][k] = df['meta_critic'][k] / 10
    elif df['meta_critic'][k] == -1:
        pass



#Remove rows with 8 or more NaNs in it
df.dropna(axis=0, how='any', thresh = 4, inplace=True)

#Save CSV, cleaned version
print('Saving CSV cleaned version')
df.to_csv("/DATA/game_price_scrap/preprocessing/cleaned_data.csv", index=False)












        






