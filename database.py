"""
Database module for user authentication
Handles SQLite operations for signup and login
"""

import sqlite3
import bcrypt
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="users.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create users table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def signup(self, username, password):
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        
        try:
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            
            conn.commit()
            conn.close()
            
            return True, "Signup successful"
        
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, f"Signup failed: {str(e)}"
    
    def login(self, username, password):
        """
        Authenticate a user
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT password_hash FROM users WHERE username = ?',
                (username,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, "Invalid username or password"
            
            password_hash = result[0]
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                return True, "Login successful"
            else:
                return False, "Invalid username or password"
        
        except Exception as e:
            return False, f"Login failed: {str(e)}"
    
    def user_exists(self, username):
        """Check if a user exists"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id FROM users WHERE username = ?',
                (username,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
    
    def get_all_users(self):
        """Get list of all usernames"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT username FROM users')
            results = cursor.fetchall()
            conn.close()
            
            return [row[0] for row in results]
        
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
