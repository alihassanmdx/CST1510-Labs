import bcrypt
import os
import secrets
import time

sessions = {}
USER_DATA_FILE = "users.txt"

wrong_attempts = {}
LOCK_DURATION = 300
MAX_ATTEMPTS = 3


def hash_password(plain_text_password):
    # Encode the password to bytes (bcrypt requires byte strings)
    password_in_bytes = plain_text_password.encode('utf-8')

    # Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt.hashpw()
    hashed_pass = bcrypt.hashpw(password_in_bytes, salt)

    # Decode the hash back to a string to store in a text file
    return hashed_pass.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    # This function extracts the salt from the hash and compares

    # Encode both values to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Validate password using bcrypt
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def register_user(username, password, role="user"):
    # Check if user already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    # Hash the password
    hashed = hash_password(password)

    # Append new user to file in format: username,hash
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed},{role}\n")

    print(f"Success: User ''{username}' registered as '{role}' Successfully.")
    return True


def user_exists(username):
    # If file does not exist → no users yet
    if not os.path.exists(USER_DATA_FILE):
        return False

    # Read file and check each line
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]  # username is before the comma
            if stored_username == username:
                return True

    return False


def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users are registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue

            stored_username = parts[0]
            stored_hash = parts[1]

            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome '{username}'!.")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    print("Error: Username not found.")
    return False


def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Error: Username characters must be 3–20."

    if not username.isalnum():
        return False, "Error: Username can only contain letters and numbers."

    return True, ""


def validate_password(password):
    if len(password) < 6 or len(password) > 50:
        return False, "Error: Password characters must be 6–50."

    if not any(c.isdigit() for c in password):
        return False, "Error: Password must contain at least one number."

    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter."

    return True, ""


def display_menu():
    print("\n" + "=" * 50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def check_password_strength(password):
    length_score = 1 if len(password) >= 8 else 0

    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    special = any(not c.isalnum() for c in password)

    score = length_score + upper + lower + digit + special

    if score <= 2:
        return "Weak"
    elif score in [3, 4]:
        return "Medium"
    else:
        return "Strong"


def login_user_with_lock(username, password):
    if username in wrong_attempts:
        count, lock_time = wrong_attempts[username]
        if count >= MAX_ATTEMPTS:
            if time.time() - lock_time < LOCK_DURATION:
                print(f"Account '{username}' is locked. Try again later.")
                return False
            else:
                # Reset after lock duration
                wrong_attempts[username] = (0, 0)

    success = login_user(username, password)

    if not success:
        if username not in wrong_attempts:
            wrong_attempts[username] = (1, 0)
        else:
            count, _ = wrong_attempts[username]
            if count + 1 >= MAX_ATTEMPTS:
                wrong_attempts[username] = (count + 1, time.time())
                print(f"Account' {username}' is now locked for 5 minutes.")
            else:
                wrong_attempts[username] = (count + 1, 0)
    else:
        # Reset on successful login
        if username in wrong_attempts:
            wrong_attempts.pop(username)

    return success


def create_session(username):
    token = secrets.token_hex(16)
    sessions[username] = token
    return token


def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            #Validate Role
            role = input("Enter role (user/admin/analyst) [default: user]: ").strip().lower()
            if role not in ["user", "admin", "analyst"]:
                role = "user"

            register_user(username, password, role)

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if login_user_with_lock(username, password):
                token = create_session(username)
                print(f"\nYou are now logged in. Session token: {token}")
                input("Press Enter to return to the main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


main()
