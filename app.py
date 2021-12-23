from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
addedMovies  = []
movieRatings = []
moviesData   = joblib.load('DataSet/moviesData.pkl')
similarities = joblib.load('DataSet/similarities.pkl')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add/', methods=['GET','POST'])
def add():
    rating = int(request.form.get('rating'))
    movie  = request.form.get('movie_name').lower() + ' '
        
    if movie not in moviesData['title'].unique():
        return render_template('index.html', text = "The film is not in our database")
    else:
        movieRatings.append(tuple((movie, rating)))
        addedMovies.append(movie)
        return render_template('index.html', text = "Successfully added!", addedMovies = addedMovies)

@app.route('/prediction/', methods=['GET','POST'])
def prediction():
    similarMovies = pd.DataFrame()

    for movie,rating in movieRatings:
        similarMovies = similarMovies.append(getSimilarMovies(movie,rating), ignore_index=True)
    
    similarMovies = similarMovies.sum().sort_values(ascending=False)
    similarMovies = similarMovies.index.tolist()
    similarMovies = [x for x in similarMovies if x not in addedMovies]
    return render_template('recommended.html', my_list = similarMovies[:10])

def getSimilarMovies(movie_name, user_rating):
    similar_score=similarities[movie_name]*(user_rating-2.5)
    similar_score=similar_score.sort_values(ascending=False)
    return similar_score

if __name__ == '__main__':
    app.run()