#%%
###CREATING A ROBUST SQLite SETUP THAT HANDLES THE SCHEMA AND CONNECTIONS###

#Importing necessary libraries
import sqlite3
import os
from datetime import datetime

from matplotlib.artist import get

#Defining the path to the database file
#We use os.path to ensure it works on both Windows and Mac/Linux automatically
DB_NAME = "news.db"
DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER,DB_NAME)

#Connection to the database
def get_db_connection():
    """
    Establishes the connection to the SQLite database.
    Returns: sqlite3.Connection object
    """
    #Checking if the data folder exits, if not, create it
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    conn = sqlite3.connect(DB_PATH)

    #This allows us to acces the columns by name instead of index
    conn.row_factory = sqlite3.Row

    return conn

#%%
#Creating the tables in the database
def create_tables():
    """
    Creates the necessary tables if they do not exist.
    Schema designed for:
    1. Uniqueness (preventing duplicates via URL)
    2. Audit trail (knowing WHEN we scraped the data)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    #Creating the articles table
    create_articles_table = """
    CREATE TABLE IF NOT EXISTS articles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    source TEXT,
    published_date TEXT,
    scraped_at TEXT
    );
    """

    cursor.execute(create_articles_table)
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_PATH}")

#%%
#Inserting an article
def insert_article(title, url, source="unknown", published_date = None):
    """
    Insert a new article into database.
    Returns: True if inserted, False if it was a duplicate
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    #Getting the current timestamp for the audit trail
    scraped_at = datetime.utcnow().isoformat()

    try:
        cursor.execute("""
            INSERT INTO articles (title, url, source, published_date, scraped_at) 
            VALUES (?, ?, ?, ?, ?)
        """, (title, url, source, published_date, scraped_at))
        
        conn.commit()
        print(f"Saved {title[:30]}...")
        return True
    except sqlite3.IntegrityError:
        #This will happen if the URL already exists(Uniqueness)
        print(f"Duplicate found(skipped): {url}")
    finally:
        conn.close()

#%%
#TEST BLOCK
#Testing the code
if __name__ == "__main__":
    create_tables()

    #Testing with dummy data
    print("--- Testing Insert ---")
    insert_article("Test Headline 1", "http://example.com/1", "TechCrunch")
    insert_article("Test Headline 1", "http://example.com/1", "TechCrunch") # Should fail (duplicate)
#%%