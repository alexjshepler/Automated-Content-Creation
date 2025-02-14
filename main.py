from Settings import load_settings
from Fetch_From_Reddit import fetch_reddit_posts

def main():
    # Load or create settings
    settings = load_settings()

    # Fetch posts from reddit using loaded settings
    fetch_reddit_posts(settings)

if __name__ == '__main__':
    main()