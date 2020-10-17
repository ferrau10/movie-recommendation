import sqlalchemy as sql
import requests
import re
import json

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
        genres.append('Drama')
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

#print(get_movies_by_genre('Fantasy'))

#print(movies)

# def random_recommander(num):
#     import random
#     result = random.choices(movies, k=num)
#     return result
