import sqlite3
import pandas as pd
import os
import streamlit as st

# 1. BULLETPROOF PATHING
# This dynamically finds the absolute path of the 'database' folder, 
# ensuring Streamlit always reads/writes to the exact same file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "system_data.db")

def init_db():
    """Creates the database folder and the initial tables if they don't exist."""
    os.makedirs(BASE_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Review TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyzed_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Review TEXT NOT NULL,
            Score INTEGER,
            Status TEXT,
            Sentiment TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_raw_reviews(df):
    """Appends a dataframe of new reviews to the raw_reviews table."""
    conn = sqlite3.connect(DB_PATH)
    # Using index=False ensures we don't accidentally write the pandas row numbers
    df.to_sql("raw_reviews", conn, if_exists="append", index=False)
    conn.close()

def load_raw_reviews():
    """Fetches the raw reviews from the database."""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM raw_reviews", conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        # 2. NO MORE SILENT ERRORS
        # If it fails, it will now explicitly tell us why on the UI
        st.error(f"🛠️ DB Read Error: {e}")
        return pd.DataFrame()

def save_analyzed_reviews(df):
    """Saves the analyzed dataframe to the database, replacing old results."""
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("analyzed_reviews", conn, if_exists="replace", index=False)
    conn.close()

def load_analyzed_reviews():
    """Fetches the analyzed reviews."""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM analyzed_reviews", conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        st.error(f"🛠️ DB Read Error: {e}")
        return pd.DataFrame()

def clear_database():
    """Deletes all records from both tables to reset the system."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM raw_reviews")
    cursor.execute("DELETE FROM analyzed_reviews")
    conn.commit()
    conn.close()

def load_top_reviews(limit=20000):
    """Fetches only the top reviews sorted by score directly from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Let SQLite do the heavy sorting instantly
    query = f"SELECT * FROM analyzed_reviews ORDER BY Score DESC LIMIT {limit}"
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        import streamlit as st
        st.error(f"🛠️ DB Read Error: {e}")
        return pd.DataFrame() 