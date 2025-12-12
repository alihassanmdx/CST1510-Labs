class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""

    def __init__(self, username: str, password_hash: str, role: str):
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role

    def get_username(self) -> str:
        """Return the username."""
        return self.__username

    def get_role(self) -> str:
        """Return the user role."""
        return self.__role

    def verify_password(self, plain_password: str, hasher) -> bool:
        """
        Check if a plain-text password matches the stored password hash.
        `hasher` must provide check_password(plain, hashed) -> bool.
        """
        return hasher.check_password(plain_password, self.__password_hash)

    def __str__(self) -> str:
        """String representation for debugging."""
        return f"User({self.__username}, role={self.__role})"
