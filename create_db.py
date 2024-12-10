import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("movie.db")
cursor = conn.cursor()

# Create movies table with rating column
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating REAL DEFAULT 0.0
)
""")

# Insert sample movies with ratings
cursor.executemany("""
INSERT INTO movies (title, genre, rating) VALUES (?, ?, ?)
""", [
    ("The Shawshank Redemption", "Drama", 9.3),
    ("The Dark Knight", "Action", 9.0),
    ("Inception", "Sci-Fi", 8.8),
    ("Forrest Gump", "Drama", 8.8),
    ("The Matrix", "Sci-Fi", 8.7),
    ("Pulp Fiction", "Crime", 8.9),
    ("Gladiator", "Action", 8.5),
    ("Titanic", "Romance", 7.8)
])

conn.commit()
conn.close()

print("Database created and populated successfully with ratings!")
