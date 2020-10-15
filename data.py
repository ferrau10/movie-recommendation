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

def get_images():
    query = sql.text("SELECT * FROM links LIMIT 4")
    results = engine.execute(query)
    uri = 'https://imdb-api.com/en/API/Images/k_uekfxuke/tt'
    titles = []
    images = []
    for i in results:
        #print(list(i))
        output = str(i[1]).rjust(7, '0')
        #movies.append(uri+output)
        url = uri+output
        #resp = requests.get(url)
        #image = resp.json()['items'][0]['image']
        #title = resp.json()['items'][0]['title']
        image = "https://f4.bcbits.com/img/0002211150_10.jpg"
        title = "Gummi Bär"
        titles.append(title)
        images.append(image)
    return (titles, images)

print(get_popular_tags())

#print(movies)

# def random_recommander(num):
#     import random
#     result = random.choices(movies, k=num)
#     return result
