import os
import sqlite3

# Helper func to create db connection
def db_connection():
    conn = sqlite3.connect('categories.db')
    cursor = conn.cursor()
    return conn, cursor

# Create the database and the Table
def create_db():
    # if the db already exists delete it first
    if 'categories.db' in os.listdir():
        os.remove('categories.db')
    conn, cursor = db_connection()
    with conn:
        # create Table
        cursor.execute('''
                       CREATE TABLE categories (
                       category_id integer PRIMARY KEY,
                       category_name text NOT NULL,
                       category_level integer NOT NULL,
                       bestoffer_enabled text NOT NULL,
                       parent_id integer NOT NULL
                       )
                       ''')

# Save categories inside db table
def save_categories(data):
    # connect to the db
    conn, cursor = db_connection()
    with conn:
        # Begin a transaction for database optimization
        cursor.execute('BEGIN TRANSACTION')
        # insert categories
        for category in data:
            cursor.execute(
                '''INSERT INTO categories VALUES
                (:category_id, :category_name, :category_level, :bestoffer_enabled, :parent_id)''',
                {'category_id': category.get('id'), 'category_name': category.get('name'),
                 'category_level': category.get('level'),
                 'bestoffer_enabled': category.get('offer'), 'parent_id': category.get('parentId')})

# Get all categories
def get_all_categories():
    conn, cursor = db_connection()
    cursor.execute('SELECT * FROM categories')
    return cursor.fetchall()

# Get category by id
def get_category_by_id(parentId):
    conn, cursor = db_connection()
    cursor.execute('SELECT * FROM categories WHERE parent_id=:parent_id', {'parent_id': parentId})
    return cursor.fetchall()
