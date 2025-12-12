import bcrypt
from models.user import User
class SimpleHasher:
    """Handles password hashing and verification."""

    def hash_password(self, plain):
        """Hash a plain text password."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, plain, hashed):
        """Check if password matches hash."""
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

class AuthManager:
    """Handles user registration and login."""

    def __init__(self, db):
        self.db = db
        self.hasher = SimpleHasher()

    def register_user(self, username, password, role="user"):
        """Register a new user with hashed password."""
        password_hash = self.hasher.hash_password(password)
        self.db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )

    def login_user(self, username, password):
        """Login a user; returns a User object if successful, else None."""
        row = self.db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if row is None:
            return None

        username_db, password_hash_db, role_db = row

        if self.hasher.check_password(password, password_hash_db):
            return User(username_db, password_hash_db, role_db)
        else:
            return None
