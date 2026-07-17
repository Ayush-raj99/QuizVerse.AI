import sqlite3

DATABASE_NAME = "users.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Check user limit
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count >= 20:
        conn.close()
        return False, "Maximum 20 users reached"

    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return True, "User created successfully"

    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists"


def check_user(username, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return True

    return False

if __name__ == "__main__":
    create_database()
    print("Database created successfully!")