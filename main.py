from Settings import load_settings
from Reddit import Reddit
from Database import create_post_db, create_script_db
from Podcast import generate_scripts

def main():
    create_script_db()
    create_post_db()
    
    settings = load_settings()
    reddit = Reddit(settings)
    
    # reddit.fetch_all_posts()
    
    generate_scripts(settings)
    

if __name__ == '__main__':
    main()