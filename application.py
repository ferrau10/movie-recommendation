from flask import Flask, render_template, request
import data
from itertools import product   

# instantiate a Flask application
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    titles, images, genres = data.get_movies()
    tags = data.get_popular_tags()
    return render_template('index.html', movies=list(zip(titles, images)), tags=tags)
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
    filter = request.form['filter']
    for i in product([1,2,3,4], [1,2,3,4]):
        ratings[i]=request.form[str(i[0])+'_'+str(i[1])]
    print(ratings)

    #data.set_user_ratings(user, ratings)

    titles, images, genres = data.get_movies_by_genre(filter)
    tags = data.get_popular_tags()
    return render_template('index.html', movies=list(zip(titles, images, genres)), tags=tags, from_filter=1)

@app.route('/images')
def images():
    return render_template('images.html')


if __name__ == '__main__':
    user_id=900
    app.run(port=80, debug=True)

