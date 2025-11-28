# Week 7: Secure Authentication System  
Student Name: Ali Hassan  
Student ID: M01096927  
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform  

## Project Description
This project is a command-line authentication system that securely handles
user registration and login. All passwords are hashed using bcrypt with automatic
salt generation to ensure strong protection against attacks.

## Features
- Secure password hashing using bcrypt
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- Persistent storage using a text file (`users.txt`)

## Technical Implementation
- **Hashing Algorithm:** bcrypt (with automatic salt)
- **Data Storage:** `users.txt` (username,hashed_password)
- **Password Security:** One-way hashing (no plaintext stored)
- **Validation Rules:**
  - Username: 3–20 alphanumeric characters
  - Password: 6–50 characters, must contain letters and numbers
