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
            subreddit TEXT NOT NULL
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            has_script BOOLEAN DEFAULT FALSE
        )
        """
    )
    
    conn.commit()
    conn.close()