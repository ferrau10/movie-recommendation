# Retrain the NMF Movie Recommender model based on new input

import pickle
import sqlalchemy as sql
import pandas as pd 
from sklearn.decomposition import NMF

# 1. Loading the data from the postgres db


with open('config.json') as config:
    data = json.load(config)
    HOST = data['database-connection']['HOST']
    USERNAME = data['database-connection']['USERNAME']    
    PORT = data['database-connection']['PORT']
    DB = data['database-connection']['DB']
    PASSWORD = data['database-connection']['PASSWORD']

engine = sql.create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')
query = sql.text("SELECT * FROM ratings")
results = engine.execute(query)

df = pd.DataFrame(results)

movies = pd.read_csv('ml-latest-small/movies.csv')


# 2. Transform the data to get it ready to fit the model

def feature_eng(ratings_df, movie_df): 
    ratings_df.columns = ['userId', 'movieId', 'rating', 'timestamp']
    unique = pd.DataFrame(ratings_df.movieId.unique())
    unique.columns = ['movieId'] 
    movies = movie_df.merge(unique, how='right')
    ratings_df = pd.merge(ratings_df, movie_df, on='movieId')
    movies = ratings_df 
    ratings_df = ratings_df.drop('timestamp', axis =1)
    ratings_df = ratings_df.pivot(index='userId', columns='movieId', values='rating')
    med_values = ratings_df.median().median()
    ratings_df = ratings_df.fillna(med_values)
    
    return ratings_df

df = feature_eng(df, movies)


#3. Re-Train and save the model

m = NMF(n_components=30)
m.fit(df)
pickle.dump(m, open('nmf_small.m', 'wb'))
