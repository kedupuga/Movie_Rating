import sqlite3
import pandas as pd

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect("movie_recommendation_system.db")
    conn.row_factory = sqlite3.Row  # This allows column access by name
    return conn

# Initialize the database (create tables, insert sample data)
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS Movies")
        cursor.execute("DROP TABLE IF EXISTS Ratings")
    except sqlite3.Error as e:
        print(f"Error during table deletion: {e}")

    # Create Movies and Ratings tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES Movies (id)
        )
    ''')

    # Insert sample movies
    movies = [
        {'title': 'Avengers', 'genre': 'Action'},
        {'title': 'RRR', 'genre': 'Drama'},
        {'title': 'Inception', 'genre': 'Sci-Fi'},
        {'title': 'The Dark Knight', 'genre': 'Action'},
        {'title': 'Interstellar', 'genre': 'Sci-Fi'}
    ]
    cursor.executemany("INSERT INTO Movies (title, genre) VALUES (?, ?)", [(m['title'], m['genre']) for m in movies])

    # Insert sample ratings
    ratings = [
        {'user_id': 1, 'movie_id': 1, 'rating': 5},
        {'user_id': 1, 'movie_id': 2, 'rating': 4},
        {'user_id': 2, 'movie_id': 1, 'rating': 4},
        {'user_id': 2, 'movie_id': 3, 'rating': 5},
        {'user_id': 3, 'movie_id': 4, 'rating': 5},
        {'user_id': 3, 'movie_id': 5, 'rating': 4}
    ]
    cursor.executemany(
        "INSERT INTO Ratings (user_id, movie_id, rating) VALUES (?, ?, ?)",
        [(r['user_id'], r['movie_id'], r['rating']) for r in ratings]
    )

    conn.commit()
    conn.close()

# Fetch all movies
def get_all_movies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movies")
    movies = cursor.fetchall()
    conn.close()
    return movies

# Fetch movie details by movie_id
def get_movie_by_id(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return movie

# Fetch ratings by movie_id
def get_ratings_by_movie_id(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ratings WHERE movie_id = ?", (movie_id,))
    ratings = cursor.fetchall()
    conn.close()
    return ratings

# Add a new rating
def add_rating(user_id, movie_id, rating):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Ratings (user_id, movie_id, rating) VALUES (?, ?, ?)", (user_id, movie_id, rating))
    conn.commit()
    conn.close()

# Update movie details
def update_movie(movie_id, title, genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Movies SET title = ?, genre = ? WHERE id = ?", (title, genre, movie_id))
    conn.commit()
    conn.close()

# Delete a movie by id
def delete_movie(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Movies WHERE id = ?", (movie_id,))
    cursor.execute("DELETE FROM Ratings WHERE movie_id = ?", (movie_id,))
    conn.commit()
    conn.close()

# Get the user-movie rating matrix
def get_user_movie_matrix():
    conn = get_db_connection()
    ratings_df = pd.read_sql_query("SELECT user_id, movie_id, rating FROM Ratings", conn)
    conn.close()
    return ratings_df

# Get movie genres for a specific user
def get_user_genre_preferences(user_id):
    conn = get_db_connection()
    query = '''
        SELECT M.genre, AVG(R.rating) as avg_rating
        FROM Ratings R
        JOIN Movies M ON R.movie_id = M.id
        WHERE R.user_id = ?
        GROUP BY M.genre
        ORDER BY avg_rating DESC
        LIMIT 3
    '''
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    genres = cursor.fetchall()
    conn.close()
    return [genre['genre'] for genre in genres]
