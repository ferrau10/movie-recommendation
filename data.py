import sqlalchemy as sql
import requests
import re

# print(sql.__version__)

HOST = '34.89.195.148'
USERNAME = 'postgres'
PORT = '5432'
DB = 'moviedb'
PASSWORD = 'postgres'

engine = sql.create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')

query = sql.text("SELECT * FROM links LIMIT 3")
results = engine.execute(query)

uri = 'https://www.imdb.com/title/tt'

movies =[]
for i in results:
    #print(list(i))
    output = str(i[1]).rjust(7, '0')
    #movies.append(uri+output)
    resp = requests.get(uri+output)
    pattern = '<div class="poster"><a href="(\\w.*?)">'
    #<img alt="[\\w.*?]src="(\\w.*?)">'
    img = re.findall(pattern, resp.text)
    print(img)


print(movies)

# def random_recommander(num):
#     import random
#     result = random.choices(movies, k=num)
#     return result


<div class="poster">
<a href="/title/tt0114709/mediaviewer/rm3813007616?ref_=tt_ov_i"> <img alt="Toy Story Poster" title="Toy Story Poster" src="https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_UX182_CR0,0,182,268_AL_.jpg">
<img alt="Toy Story Poster" title="Toy Story Poster" src="https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_UX182_CR0,0,182,268_AL_.jpg"></a>    </div>