from operator import mod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pickle
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import cleaning_functions as cf
from nltk.stem.snowball import SnowballStemmer
import joblib
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

import warnings; warnings.simplefilter('ignore')

def modeling_sim():
    #Import dataset
    df = pd.read_csv('./preprocessing/cleaned_data.csv')

    #Select the columns you need
    df = df[['title', 'Genre', 'Developer', 'Publisher', 'Download size', 'How Long To Beat', 'ESRB Rating','Description', 'meta_critic', 'meta_user']]

    #Turn whole dataset into string format
    df = df.astype(str)

    #Add commas between the variables, just to declare them as separate words
    df['soup'] = df['Genre'] + ', ' + df['Developer'] + ', ' + df['Publisher'] + ', ' + df['Download size'] + ', ' + df['Description'] + ' ' + df['meta_critic'] + ' ' + df['meta_user']

    #Clean data for description
    df['soup'] = df['soup'].apply(cf.remove_between_square_brackets)

    # Not sure we need this one?
    df['soup'] = df['soup'].apply(cf.rem_special_char)
    df['soup'] = df['soup'].apply(cf.lower_case)
    df['soup'] = df['soup'].apply(cf.stemmer)
    df['soup'] = df['soup'].apply(cf.lemmo)


    #TDIDF vectorizer
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['soup'])


    #adding a linear kernel to the tdidf matrix, looking at the correlations after
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # joblib.dump(cosine_sim, 'demo_model_2.pkl')

# modeling_sim()
#saving dataframe, and similarity matrix
# pickle.dump(df,open('game_list.pkl','wb'))
# pickle.dump(cosine_sim,open('similarity_2.pkl','wb'))











