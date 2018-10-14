import os
import sqlite3

# Helper func to create db connection
def db_connection():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    return conn, cursor

# Create the database and the Table
def create_db():
    # if the db already exists delete it first
    if 'posts.db' in os.listdir():
        os.remove('posts.db')
    conn, cursor = db_connection()
    with conn:
        # create Table
        cursor.execute('''
                       CREATE TABLE posts (
                       id integer,
                       title text,
                       body text
                       )
                       ''')

# Save posts inside db table
def save_posts(id, title, body):
    # connect to the db
    conn, cursor = db_connection()
    with conn:
        # insert data
        cursor.execute('INSERT INTO posts VALUES (:id, :title, :body)',
                       {'id': id, 'title': title, 'body': body})

# Get all posts
def get_all_posts():
    conn, cursor = db_connection()
    cursor.execute('SELECT * FROM posts')
    return cursor.fetchall()

# Get post by id
def get_post_by_id(postid):
    conn, cursor = db_connection()
    cursor.execute('SELECT * FROM posts WHERE id=:id', {'id': postid})
    return cursor.fetchone()
