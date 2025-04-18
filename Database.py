import sqlite3 as sql

DB_NAME = 'posts.db'

# Create the database and the 'posts' table if it doesn't exist
def create_post_db():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    
    """
    Create table if it doesn't exist
    
    Columns:
        - id | Post ID (TEXT, primary key, not null)
        - author | Author of the post, [deleted] if the author doesn't exist (TEXT, not null)
        - subreddit | The subreddit where the post was posted (TEXT, not null)
        - title | The title of the post (TEXT, not null)
        - content | The content of the post (TEXT, not null)
        - has_script | If a script has been generated for this post (BOOLEAN, default false)
    """
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            author TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            has_script BOOLEAN DEFAULT FALSE
        )
        """
    )
    
    conn.commit()
    conn.close()

# Create the database and the 'scripts' table if it doesn't exist
def create_script_db():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    """
    Create table if it doesn't exist
    
    Columns:
        - id | Post ID (TEXT, primary key, not null)
        - author | Author of the post, [deleted] if the author doesn't exist (TEXT, not null)
        - subreddit | The subreddit where the post was posted (TEXT, not null)
        - title | The title of the post (TEXT, not null)
        - content | The content of the post (TEXT, not null)
        - script | The generated script (TEXT, not null)
        - has_audio | If the audio has been generated (BOOLEAN, default false)
    """

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scripts (
            id TEXT PRIMARY KEY,
            author TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            script TEXT NOT NULL,
            has_audio BOOLEAN DEFAULT FALSE
        )
        """
    )

# Insert a new post
def insert_post(post):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT OR IGNORE INTO posts (id, author, subreddit, title, content, has_script)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (post['id'], post['author'], post['subreddit'], post['title'], post['content'], False)
    )
    
    conn.commit()
    conn.close()
    
def insert_script(script):
    pass