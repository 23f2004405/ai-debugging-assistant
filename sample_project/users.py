import sqlite3

DB = "app.db"

def create_user(name: str, email: str):
    conn = sqlite3.connect(DB)
    try:
        # BUG: the UNIQUE constraint can raise an IntegrityError.
        conn.execute(
            "INSERT INTO users(name, email) VALUES (?, ?)",
            (name, email),
        )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

def get_user_by_email(email: str):
    conn = sqlite3.connect(DB)
    try:
        return conn.execute(
            "SELECT id, name, email FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    finally:
        conn.close()
