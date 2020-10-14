from flask import Flask, render_template, request
import data

# instantiate a Flask application
app = Flask(__name__)

# trigger hello function every time somebody visits \home on my website
@app.route('/home')
def hello():
    movie_rec = data.random_recommander(3)
    print(movie_rec)
    return render_template('home.html', results=movie_rec)

@app.route('/index2')
def hell():
    #movie_rec = data.random_recommander(3)
    #print(movie_rec)
    return render_template('index2.html')

@app.route('/', methods = ['POST', 'GET'])
def index():
    #print(request.args['fname'])
    print(request.form['fname'])
    return render_template('index.html', text=request.form['fname'])

if __name__ == '__main__':
    app.run(port=80, debug=True)

