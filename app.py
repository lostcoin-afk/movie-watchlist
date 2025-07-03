from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
OMDB_API_KEY = '4f7ff4d5'
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    plot = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form['title']
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
    data = response.json()
    if response.status_code !=200:
        return "Error fetching movie data from OMDB API.", 500
    if data['Response'] == 'False':
        return f"Movie not found: {data['Error']}", 404
    movie = Movie(
        title=data['Title'],
        year=int(data['Year']),
        director=data['Director'],
        genre=data['Genre'],
        rating=float(data['imdbRating']),
        plot=data['Plot']
    )
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('index'),)

@app.route('/plot/<int:movie_id>')
def plot_page(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    return redirect('index.html', movie=movie)

@app.route('/delete/<int:movie_id>')
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

import os
if __name__ == '__main__':
    if not os.path.exists("movies.db"):
        with app.app_context():
            db.create_all()
            print("📀 Database initialized.")
    else:
        with app.app_context():
            db.create_all()
            print("✅ Database created successfully!")
    app.run(debug=True)

