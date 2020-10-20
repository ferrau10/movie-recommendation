import sqlalchemy as sql
import requests
import re
import json
import pickle 
import numpy as np
import pandas as pd

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
    query = sql.text("SELECT * FROM links LIMIT 4")
    results = engine.execute(query)
    uri = 'https://imdb-api.com/en/API/Images/k_uekfxuke/tt'
    titles = []
    images = []
    genres = []
    for i in results:
        output = str(i[1]).rjust(7, '0')
        url = uri+output
        #resp = requests.get(url)
        #print(resp.json())
        #image = resp.json()['items'][0]['image']
        #title = resp.json()['items'][0]['title']
        image = "https://f4.bcbits.com/img/0002211150_10.jpg"
        #title = "Gummi Bär"
        title = i[0] 
        titles.append(title)
        images.append(image)
        genres.append(' ')
    return (titles, images, genres)



def get_movies_by_genre(genre="%"):
    query = sql.text(f"SELECT * FROM links, movies WHERE movies.movieid = links.movieid AND movies.genres LIKE '{genre}' LIMIT 4")
    results = engine.execute(query)
    uri = 'https://imdb-api.com/en/API/Images/k_uekfxuke/tt'
    titles = []
    images = []
    genres = []
    for i in results:
        output = str(i[1]).rjust(7, '0')
        url = uri+output
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
    return (titles, images, genres)


def get_image_by_id(movieid="%"):
    query = sql.text(f"SELECT * FROM links, movies WHERE movies.movieid = links.movieid AND movies.movieid = '{movieid}'")
    results = engine.execute(query)
    uri = 'https://imdb-api.com/en/API/Images/k_edey695y/tt'

    for i in results:
        output = str(i[1]).rjust(7, '0')
        url = uri+output
        resp = requests.get(url)
        print(resp.json())
        print(resp.json()['items'][0]['image'])
        image = resp.json()['items'][0]['image']
    return image

# def set_user_ratings(user=900, ratings):
#     pass

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
    this function gets a user Id, and returns n movie titles and their ids based on the user's ratings
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
    
    for i in range(n):
        moviename= user_input['title'].iloc[i]
        return_list_name.append(moviename)
    
    return_list_id = []
    
    for i in range(n):
        movieId = user_input.movieId.iloc[i]
        return_list_id.append(movieId)

    return return_list_name, return_list_id

