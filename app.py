from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("movie.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=["POST"])
def recommend():
    genre = request.form.get("genre")
    conn = get_db_connection()
    movies = conn.execute("SELECT title FROM movies WHERE genre = ? ORDER BY rating DESC", (genre,)).fetchall()
    conn.close()
    return render_template("recommendations.html", genre=genre, movies=[movie["title"] for movie in movies])

@app.route('/movies')
def movie_list():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return render_template("movie_list.html", movies=movies)

@app.route('/add', methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form.get("genre")
        rating = request.form.get("rating", 0.0)
        conn = get_db_connection()
        conn.execute("INSERT INTO movies (title, genre, rating) VALUES (?, ?, ?)", (title, genre, float(rating)))
        conn.commit()
        conn.close()
        return redirect("/movies")
    return render_template("add_movie.html")

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update_movie(id):
    conn = get_db_connection()
    movie = conn.execute("SELECT * FROM movies WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        title = request.form.get("title")
        genre = request.form.get("genre")
        rating = request.form.get("rating", 0.0)
        conn.execute("UPDATE movies SET title = ?, genre = ?, rating = ? WHERE id = ?", (title, genre, float(rating), id))
        conn.commit()
        conn.close()
        return redirect("/movies")
    conn.close()
    return render_template("update_movie.html", movie=movie)

@app.route('/delete/<int:id>', methods=["GET"])
def delete_movie(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM movies WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/movies")

if __name__ == "__main__":
    app.run(debug=True)
