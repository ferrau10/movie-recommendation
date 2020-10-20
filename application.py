from flask import Flask, render_template, request
import data
from itertools import product   

# instantiate a Flask application
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    titles, images, genres, ids = data.get_movies()
    tags = data.get_popular_tags()
    return render_template('index.html', movies=list(zip(titles, images, ids)), tags=tags)
    #return render_template('index.html')
  
@app.route('/recommend', methods = ['POST', 'GET'])      
def recommend():
    print(request.args['userid'])
    #fname = 'John'
    #print(request.form['fname'])
    return render_template('recommend.html')

# trigger hello function every time somebody visits \home on my website
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

@app.route('/images')
def images():
    return render_template('images.html')



@app.route('/recommendation', methods = ['POST', 'GET'])
def give_recommendation():
    recommendation = data.get_recommendations_name(1, 3)
    return render_template('recommendation.html', recommendation=zip(recommendation))
    #return render_template('index2.html')

if __name__ == '__main__':
    user_id=900
    app.run(port=80, debug=True)


