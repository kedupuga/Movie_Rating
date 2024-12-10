from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from database import get_all_movies, get_movie_by_id, get_ratings_by_movie_id, add_rating, update_movie, delete_movie, get_user_movie_matrix, get_user_genre_preferences

# Initialize Flask app
app = Flask(__name__)

# Movie recommendation function (based on both ratings and genre)
def recommend_movies(user_id, top_n=3):
    ratings_df = get_user_movie_matrix()

    # Create user-movie matrix
    user_movie_matrix = ratings_df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)

    # Calculate similarity between users
    user_similarity = cosine_similarity(user_movie_matrix)
    similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

    # Get similar users
    similar_users = similarity_df[user_id].sort_values(ascending=False).index[1:]

    # Aggregate ratings from similar users for recommendation
    user_ratings = user_movie_matrix.loc[similar_users].mean().sort_values(ascending=False)
    user_seen_movies = ratings_df[ratings_df['user_id'] == user_id]['movie_id']

    # Step 2: Identify top genres based on user ratings
    top_genres = get_user_genre_preferences(user_id)

    # Step 3: Filter recommendations by genre preference
    recommendations = user_ratings[~user_ratings.index.isin(user_seen_movies)]
    
    recommended_movie_ids = []
    for genre in top_genres:
        genre_movies = [movie['id'] for movie in get_all_movies() if movie['genre'] == genre]
        filtered_recommendations = recommendations[recommendations.index.isin(genre_movies)]
        recommended_movie_ids.extend(filtered_recommendations.index.tolist())

    recommended_movie_ids = list(set(recommended_movie_ids))

    # Fetch recommended movies
    recommended_movies = [movie for movie in get_all_movies() if movie['id'] in recommended_movie_ids]
    return recommended_movies

# Route to view all movies
@app.route('/movies')
def movies():
    movies = get_all_movies()
    return render_template('movies.html', movies=movies, page='movies')

# Route to add a new movie
@app.route('/movies/add', methods=['GET', 'POST'])
def add_movie_view():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        add_movie(title, genre)
        return redirect(url_for('movies'))
    return render_template('add_movie.html', page='add_movie')

# Route to view movie details
@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    ratings = get_ratings_by_movie_id(movie_id)
    return render_template('movie_details.html', movie=movie, ratings=ratings, page='movie_details')

# Route to add a rating
@app.route('/movies/<int:movie_id>/add_rating', methods=['GET', 'POST'])
def add_rating_view(movie_id):
    if request.method == 'POST':
        rating = request.form['rating']
        add_rating(user_id=1, movie_id=movie_id, rating=rating)
        return redirect(url_for('movie_details', movie_id=movie_id))
    return render_template('add_rating.html', movie_id=movie_id, page='add_rating')

# Route to update a movie
@app.route('/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_movie_view(movie_id):
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        update_movie(movie_id, title, genre)
        return redirect(url_for('movie_details', movie_id=movie_id))
    movie = get_movie_by_id(movie_id)
    return render_template('update_movie.html', movie=movie, page='update_movie')

# Route to delete a movie
@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie_view(movie_id):
    delete_movie(movie_id)
    return redirect(url_for('movies'))

# Route to get recommendations
@app.route('/movies/recommendations')
def recommendations():
    recommended_movies = recommend_movies(user_id=1)
    return render_template('recommendations.html', recommended_movies=recommended_movies, page='recommendations')

if __name__ == '__main__':
    app.run(debug=True)
