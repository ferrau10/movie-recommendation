from flask import Flask, render_template, request
import data
from itertools import product   


# instantiate a Flask application
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    titles, images, genres, ids = data.get_movies_by_genre("%")
    tags = data.get_popular_tags()
    return render_template('index.html', movies=list(zip(titles, images, ids, genres)), tags=tags, from_filter=1)
  

@app.route('/recommend', methods = ['POST', 'GET'])      
def recommend():
    ratings = {}
    movieids = {}
    try:
        user_id = request.args['userid']
        for i in product([1,2,3,4], [1,2,3,4]):
            ratings[i]  = request.form['rating_'+str(i[0])+'_'+str(i[1])]
            movieids[i] = request.form['movieid_'+str(i[0])+'_'+str(i[1])]
        data.set_user_ratings(movieids, ratings, 900)
    except KeyError:
        user_id = 1
    finally: 
        recommendation_name, recommendation_id = data.get_recommendations_name(user_id, 3)
        image_list = []
        for i in recommendation_id:
            image = data.get_image_by_id(i)
            image_list.append(image)
    return render_template('recommend.html', recommendation=list(zip(recommendation_name, recommendation_id, image_list)))



@app.route('/filter', methods = ['POST', 'GET'])
def filter():
    ratings = {}
    movieids = {}
    filter = request.form['filter']
    if filter == "Enter Genre.....":
        filter = "%"
    for i in product([1,2,3,4], [1,2,3,4]):
        ratings[i]  = request.form['rating_'+str(i[0])+'_'+str(i[1])]
        movieids[i] = request.form['movieid_'+str(i[0])+'_'+str(i[1])]
    data.set_user_ratings(movieids, ratings, 900)

    titles, images, genres, ids = data.get_movies_by_genre(filter)
    tags = data.get_popular_tags()
    print(list(zip(titles, images, ids, genres)))
    return render_template('index.html', movies=list(zip(titles, images, ids, genres)), tags=tags, from_filter=1)


if __name__ == '__main__':
    user_id=900
    app.run(debug=True, port=8080)


