import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("movie.db")
cursor = conn.cursor()

# Create movies table
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL
)
""")

# Insert sample movies
cursor.executemany("""
INSERT INTO movies (title, genre) VALUES (?, ?)
""", [
    ("The Shawshank Redemption", "Drama"),
    ("The Dark Knight", "Action"),
    ("Inception", "Sci-Fi"),
    ("Forrest Gump", "Drama"),
    ("The Matrix", "Sci-Fi"),
    ("Pulp Fiction", "Crime"),
    ("Gladiator", "Action"),
    ("Titanic", "Romance")
])

conn.commit()
conn.close()

print("Database created and populated successfully!")
