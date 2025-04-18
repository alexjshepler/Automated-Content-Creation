from Settings import load_settings
from Reddit import Reddit
from Database import create_post_db, create_script_db

def main():
    create_script_db()
    create_post_db()
    
    settings = load_settings()
    reddit = Reddit(settings)
    
    reddit.fetch_all_posts()

if __name__ == '__main__':
    main()