import sqlite3
import bcrypt
from pathlib import Path
from app.data.db import connect_database

def register_user(username, password, role="user"):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, f"Username '{username}' already exists."

    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    password_hash = hashed.decode("utf-8")

    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()
    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."

    stored_hash = user[2]
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(conn, filepath="DATA/users.txt"):
    """
    Migrate users from users.txt to the database.

    Args:
        conn: Database connection
        filepath: Path to users.txt file (can be string or Path object)

    Returns:
        int: Number of users successfully migrated
    """
    filepath = Path(filepath)  # Convert string to Path object
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return 0
    cursor = conn.cursor()
    migrated_count = 0
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            if len(parts) >= 3:
                username = parts[0].strip()
                password_hash = parts[1].strip()
                role = parts[2].strip()
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"  ❌ Error migrating user {username}: {e}")

    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")
    return migrated_count