from flask import Flask, render_template, request
import data

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
@app.route('/filter')
def filter():
    filter = request.args['filter']
    titles, images, genres = data.get_movies_by_genre(filter)
    tags = data.get_popular_tags()
    return render_template('index.html', movies=list(zip(titles, images, genres)), tags=tags, from_filter=1)

@app.route('/images')
def images():
    return render_template('images.html')


if __name__ == '__main__':
    app.run(port=80, debug=True)

