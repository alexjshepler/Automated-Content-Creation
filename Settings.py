import praw
import json

SETTINGS_PATH = './settings.json'

# Load settings from a JSON file or prompt the user to create one
def load_settings():
    settings = {}
    
    try:
        # Try to load settings from the JSON file
        with open(SETTINGS_PATH, 'r') as file:
            settings = json.load(file)
            
        print('\nSettings loaded successfully!\n')
        
    except FileNotFoundError:
        print("\nSettings file not found. Let's create one now!\n")
        
    except:
        print("\nUnknown error occurred\n")
        
    # If settings are not available, prompt the user to create new ones
    if not settings:
        settings = prompt_user_for_settings()
    
    # Validate settings
    settings = validate_settings(settings)
    
    # Save the settings to the JSON file
    with open(SETTINGS_PATH, 'w') as file:
        json.dump(settings, file, indent=4)
        
    return settings

# Prompt the user to enter settings and create the settings JSON file
def prompt_user_for_settings():
    print('\n----- Reddit App Settings -----')
    print("First, go to: https://www.reddit.com/prefs/apps\n")
    
    # Ask the user if they have an app created on Reddit
    while True:
        has_app = input("Do you have an app made on Reddit? (y/n)").lower()
        
        if has_app in ['y', 'n']:
            break
        else:
            print("Please enter only 'y' or 'n'")
            
    # Guide the user on creating an app on Reddit
    if has_app == 'n':
        print("\nLet's create one! Follow these steps:")
        print(
            """
        1) Go to 'are you a developer? Create an app...'
        2) Enter any name for your app, select 'script', and use any valid redirect URI (e.g., https://google.com).
        3) Complete the captcha and click 'Create app'.
        4) Once created, click 'edit app' to see your app details.
        """
        )

    # Collect app details
    print('\n----- App Details -----')
    client_id = input('Enter the app id (under the app name, next to "personal use script"): ')
    client_secret = input('Enter the app secret: ')
    username = input('Enter your Reddit username: ')
    
    # Collect user preferences for the subreddits
    subreddits = prompt_for_subreddits()
    
    # Collect user preference for the fetch method
    fetch_methods = ["top", "hot", "new", "controversial", "rising"]
    print('\n----- Fetch Method -----')
    
    while True:
        fetch_method = input(f"How do you want to fetch posts? ({', '.join(fetch_methods)}): ").lower()
        
        if fetch_method in fetch_methods:
            break
        else:
            print(f"Invalid choice, Please choose one of {', '.join(fetch_methods)}")
            
    # Return settings dictionary
    return {
        "reddit": {
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
        },
        "subreddits": subreddits,
        "fetch_method": fetch_method,
    }

# Prompt the user for subreddit prefrence
def prompt_for_subreddits():
    subreddits = []
    
    print('\n----- Subreddit Preferences -----')
    print("You can enter subreddit names or links, separated by commas, or enter one subreddit at a time")
    print("To stop, type '!quit'")
    
    while True:
        # Ask user to input subreddits either separated by commas or one at a time
        sub_input = input("Enter subreddit(s): ")
        
        if sub_input.lower() == '!quit':
            break
        
        # Check if input has multiple subreddits
        if ',' in sub_input:
            subreddits.extend([item.strip() for item in sub_input.split(',')])
        else:
            if sub_input != '':
                subreddits.append(sub_input.strip())
                
    # Normalize subreddits
    subreddits = [
        sub.replace("https://www.reddit.com/r/", "")
        .replace("www.reddit.com/r/", "")
        .replace("reddit.com/r/", "")
        .replace("/r/", "")
        .replace("/", "")
        .strip()
        for sub in subreddits
    ]

    print(f"Subreddits to fetch from: {subreddits}")
    return subreddits

# Validate the entered settings and prompt user to re-enter any invalid or missing settings
def validate_settings(settings):
    print('\n----- Validating Settings -----')
    
    # Check if any Reddit settings are missing
    if (
        not settings['reddit']
        or not settings['reddit']['client_id']
        or not settings['reddit']['client_secret']
        or not settings['reddit']['username']
    ):
        print('Error: Reddit app credentials are missing or incomplete. Please re-enter them now')
        
        settings = prompt_user_for_settings()
        
    # Check if subreddits are missing or empty
    if not settings.get('subreddits') or not settings['subreddits']:
        print("Error: No subreddits specified. Please re-enter them now")
        settings['subreddits'] = prompt_for_subreddits()
        
    # Validate fetch method
    fetch_methods = ["top", "hot", "new", "controversial", "rising"]
    if settings.get('fetch_method') not in fetch_methods:
        print(f"Error: Invalid fetch method. Must be one of {', '.join(fetch_methods)}. Please re-enter it now")
        settings["fetch_method"] = input(
            f"How do you want to fetch posts? ({', '.join(fetch_methods)}): "
        ).lower()
        
    # Validate subreddits exist
    settings['subreddits'] = validate_subreddits(settings['subreddits'], settings['reddit'])
    
    print("Settings validated successfully!\n")

# Validate that each subreddit exists
def validate_subreddits(subreddits, reddit_credentials):
    print('\n----- Validating Subreddits -----')
    valid_subreddits = []
    reddit = praw.Reddit(
        client_id=reddit_credentials["client_id"],
        client_secret=reddit_credentials["client_secret"],
        username=reddit_credentials["username"],
        user_agent="RedditAppValidator",
    )

    for subreddit in subreddits:
        if subreddit:
            try:
                reddit.subreddit(subreddit).id
                valid_subreddits.append(subreddit)
                print(f"Valid subreddit: {subreddit}")
            except Exception as ex:
                print(f"Warning: Subreddit '{subreddit}' is invalid. Error: {ex}")
                
    if not valid_subreddits:
        print('No valid subreddits found. Please re-enter them now')
        return prompt_for_subreddits()
    
    return valid_subreddits