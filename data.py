import sqlalchemy as sql
import requests
import re
import json
import pickle 
import numpy as np
import pandas as pd
from itertools import product  

# print(sql.__version__)

HOST = '34.89.195.148'
USERNAME = 'postgres'
PORT = '5432'
DB = 'moviedb'
PASSWORD = 'postgres'

engine = sql.create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')
query = sql.text("SELECT * FROM links LIMIT 7")
results = engine.execute(query)

def get_popular_tags():
    query = sql.text("SELECT * FROM tags LIMIT 15")
    results = engine.execute(query)
    tags=[]
    for i in results:
        tags.append(i[2])
    return tags

def get_movies():
    query = sql.text("SELECT * FROM links ORDER BY RANDOM() LIMIT 16")
    results = engine.execute(query)
    uri = 'https://imdb-api.com/en/API/Images/k_uekfxuke/tt'
    titles = []
    images = []
    genres = []
    ids = []
    for i in results:
        imdbid = str(i[1]).rjust(7, '0')
        url = uri+imdbid
        #resp = requests.get(url)
        #print(resp.json())
        #image = resp.json()['items'][0]['image']
        #title = resp.json()['items'][0]['title']
        image = "https://f4.bcbits.com/img/0002211150_10.jpg"
        title = "Gummi Bär"
        title = i[0] 
        titles.append(title)
        images.append(image)
        genres.append(' ')
        ids.append(i[0])
    return (titles, images, genres, ids)

def get_movies_by_genre(genre="%"):
    query = sql.text(f"SELECT * FROM links, movies WHERE movies.movieid = links.movieid AND movies.genres LIKE '{genre}' ORDER BY RANDOM() LIMIT 16")
    results = engine.execute(query)
    uri = 'https://imdb-api.com/en/API/Images/k_uekfxuke/tt'
    titles = []
    images = []
    genres = []
    ids = []
    for i in results:
        imdbid = str(i[1]).rjust(7, '0')
        url = uri+imdbid
        #resp = requests.get(url)
        #print(i[5])
        #image = resp.json()['items'][0]['image']
        #title = resp.json()['items'][0]['title']
        image = "https://f4.bcbits.com/img/0002211150_10.jpg"
        #title = "Gummi Bär"
        title = i[0] 
        titles.append(title)
        images.append(image)
        genres.append(i[5])
        ids.append(i[0])
    return (titles, images, genres, ids)

def set_user_ratings(movieids, ratings, userid=900):
    for i in product([1,2,3,4], [1,2,3,4]):
        rating  = ratings[i]
        movieid = movieids[i]
        query = f"INSERT INTO ratings VALUES ({userid}, {movieid}, {rating}, 1445714835) ON CONFLICT (userid, movieid) DO UPDATE SET rating = {rating};"
        if rating !="":
            print(query)
            engine.execute(query)

#print(get_movies_by_genre('Fantasy'))




#note: there are two functions, one returns movie ids, the other movies titles.

m = pickle.load(open('nmf_small.m', 'rb'))

#preparing the movies df
df = pd.read_csv('ml-latest-small/ratings.csv')
movies = pd.read_csv('ml-latest-small/movies.csv')
unique = pd.DataFrame(df.movieId.unique())
unique.columns = ['movieId'] 
movies = movies.merge(unique, how='right')
movies  = movies.drop('genres', axis = 1)


# this was previously calculated
med_values = 3.5

def get_recommendations(userId, n):

    '''
    this function gets a user Id, and returns n recommendation based on the user's ratings
    '''

    query = sql.text(f" select * from ratings WHERE userId = {userId}")
    results = engine.execute(query)
    results = pd.DataFrame(results)
    results.columns = ['userId', 'movieId', 'ratings', 'timestamp']
    results = results.drop('timestamp', axis = 1)
    user_input = results.merge(movies, how = 'right')
    user_input['input'] = user_input['ratings'].fillna(med_values)

    # make sure the new input has >1 dimension & has as many columns as there are films!
    new_user_input = np.array(user_input['input']).reshape(1,9724)
    user_P = m.transform(new_user_input)
    Q = m.components_
    user_R = np.dot(user_P, Q)
    user_R = user_R.tolist()
    user_input['recommendation'] = user_R[0]
    user_input = user_input[user_input['ratings'].isna()]
    
    return_list = []
    for i in range(n):
        movieId = user_input.movieId.iloc[i]
        return_list.append(movieId)
    
    return return_list 

# so far it took 1.11 seconds to get 3 recommendations from user 1

def get_recommendations_name(userId, n):

    '''
    this function gets a user Id, and returns n movie titles based on the user's ratings
    '''

    query = sql.text(f" select * from ratings WHERE userId = {userId}")
    results = engine.execute(query)
    results = pd.DataFrame(results)
    results.columns = ['userId', 'movieId', 'ratings', 'timestamp']
    results = results.drop('timestamp', axis = 1)
    user_input = results.merge(movies, how = 'right')
    user_input['input'] = user_input['ratings'].fillna(med_values)

    # make sure the new input has >1 dimension & has as many columns as there are films!
    new_user_input = np.array(user_input['input']).reshape(1,9724)
    user_P = m.transform(new_user_input)
    Q = m.components_
    user_R = np.dot(user_P, Q)
    user_R = user_R.tolist()
    user_input['recommendation'] = user_R[0]
    user_input = user_input[user_input['ratings'].isna()]
    
    return_list_name = []
    
    for i in range(3):
        moviename= user_input['title'].iloc[i]
        return_list_name.append(moviename)

    return return_list_name

print(get_recommendations_name(1, 4))
