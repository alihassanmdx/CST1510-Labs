from app.data.db import connect_database
import bcrypt

def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):
    """Insert new user. Expects password_hash (already bcrypt hashed)."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

def verify_user(username, plain_password):
    """Verify username + bcrypt hashed password."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return False

    stored_hash = result["password_hash"] if isinstance(result, dict) else result[0]

    # Ensure stored_hash is bytes
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()

    return bcrypt.checkpw(plain_password.encode(), stored_hash)

def get_user_role(username):
    """Retrieve the role of a user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
