import sqlite3 as sql

DB_NAME = "posts.db"
PODCAST_DB_NAME = 'podcast.db'


# Create the database and the 'posts' table if it doesn't exist
def create_db():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    # Columns:
    # id (TEXT, primary key, not null, post id)
    # author (TEXT, not null, the author of the post ([deleted] if the user no longer exists))
    # subreddit (TEXT, not null, subreddit of the post)
    # title (TEXT, not null, title of post)
    # content (TEXT, content of post)
    # score (INTEGER, score of post)
    # num_comments (INTEGER, number of comments)
    # created_utc (REAL, date posted)
    # upvode_ratio (REAL, ratio of up votes to down votes)
    # used (BOOLEAN, default false, true if used and false if not used)

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            author TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            score INTEGER,
            num_comments INTEGER,
            created_utc REAL,
            upvote_ratio REAL,
            used BOOLEAN DEFAULT FALSE
        )
        """
    )
    
    conn.commit()
    conn.close()

def create_podcast_db():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    # Columns:
    # id (TEXT, primary key, not null, post id)
    # author (TEXT, not null, the author of the post ([deleted] if the uesr no longer exists))
    # subreddit (TEXT, not null, subreddit of the post)
    # title (TEXT, not null, title of post)
    # content (TEXT, content of post)
    # script (TEXT, script that gets generated)
    # used (BOOLEAN, default false, true if used and false if not used)

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scripts (
            id TEXT PRIMARY KEY,
            author TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            script TEXT,
            used BOOLEAN DEFAULT FALSE
        )
        """
    )
    
    conn.commit()
    conn.close()

# Insert a new post or update an existing post
def insert_or_update_post(post):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO posts (id, author, subreddit, title, content, score, num_comments, created_utc, upvote_ratio, used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            score = excluded.score,
            num_comments = excluded.num_comments,
            upvote_ratio = excluded.upvote_ratio
        """,
        (
            post['id'],
            post['author'],
            post['subreddit'],
            post['title'],
            post.get('content', None),
            post.get('score', 0),
            post.get('num_comments', 0),
            post.get('created_utc', 0.0),
            post.get('upvote_ratio', 0.0),
            False
        )
    )

    conn.commit()
    conn.close()


# Insert a new script
def insert_script(post_id, post_subreddit, post_author, post_title, post_content, script):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

            # id TEXT PRIMARY KEY,
            # author TEXT NOT NULL,
            # subreddit TEXT NOT NULL,
            # title TEXT NOT NULL,
            # content TEXT,
            # script TEXT,
            # used BOOLEAN DEFAULT FALSE


    cursor.execute(
        """
        INSERT INTO scripts (id, author, subreddit, title, content, script, used)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            post_id,
            post_author,
            post_subreddit,
            post_title,
            post_content,
            script,
            False,
        ),
    )

    conn.commit()
    conn.close()


def get_fetch_method(fetch_method):
    if fetch_method == 'top':
        return 'score'
    elif fetch_method == 'new':
        return 'created_utc'
    elif fetch_method == 'controversial':
        return 'num_comments'
    elif fetch_method == 'best':
        return 'upvote_ratio'

# Get all posts in database that haven't been used
def get_unused_posts(fetch_method):
    fetch = get_fetch_method(fetch_method)
    
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT * FROM posts WHERE used = FALSE ORDER BY ? DESC
        """,
        (fetch)
    )
    
    posts = cursor.fetchall()
    conn.close()
    return posts

# Get all posts in database
def get_all_posts(fetch_method):
    fetch = get_fetch_method(fetch_method)

    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM posts ORDER BY ? DESC
        """,
        (fetch),
    )

    posts = cursor.fetchall()
    conn.close()
    return posts

# Get all AITAH posts in database
def get_all_AITAH_posts():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM posts WHERE subreddit = ?
        """,
        ('AITAH',)
    )

    posts = cursor.fetchall()
    conn.close()

    return posts

# Check if post is in podcast database
def is_post_in_podcast_db(content):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scripts WHERE content = ?",(content,))

    posts = cursor.fetchall()
    conn.close()
    
    return len(posts) > 0


# Get a random post in database
def get_random_AITAH_post():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM posts WHERE subreddit = ? ORDER BY RANDOM() LIMIT 1
        """,
        ('AITAH',)
    )

    post = cursor.fetchone()
    conn.close()

    return post

# Get a random post in database
def get_first_unused_script():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM scripts WHERE used = ?
        """,
        (False,),
    )

    script = cursor.fetchone()
    conn.close()

    return script

# Mark a post as used
def mark_post_used(post_id):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE posts SET used = TRUE WHERE id = ?", (post_id))
    
    conn.commit()
    conn.close()
