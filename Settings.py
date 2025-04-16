import praw # Reddit api
import json

SETTINGS_PATH = './settings.json'

# Load settings the settings or create/fix them
def load_settings():
    settings = {}
    
    print('========== Loading Settings ==========')
    
    # Try to load the settings from file
    try:
        with open(SETTINGS_PATH, 'r') as file:
            settings = json.load(file)
            
        print("Loaded settings")
    except FileNotFoundError:
        print('Settings do not exist, creating them now')
    except:
        print('I dunno, something happened')
        
    # Create new settings if settings don't exist
    if not settings:
        settings = prompt_for_settings()
    
    # Validate settings
    settings = validate_settings(settings)
    
    with open(SETTINGS_PATH, 'w') as file:
        json.dump(settings, file, indent=4)
        
    return settings
    
def prompt_for_settings():
    settings = {}
    
    print('========== Getting Settings ==========')
    
    client_id, client_secret, username, subreddits = prompt_reddit()
    groq_api, model = prompt_reddit()
    elevenlabs_api, model_1, model_2 = prompt_elevenlabs()

def prompt_reddit():
    print('===== Reddit Settings\n')
    
    print("First, go to: https://www.reddit.com/prefs/apps\n")
    
    while True:
        has_app = input("Do you have an app created on Reddit? (y/n): ").lower()
        
        if has_app in ['y', 'n']:
            break
        else:
            print("Please only enter y or n\n")
            
    # Guide the user through the process of creating an app on Reddit
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
        
    print('----- Reddit Settings')
    # Collect app details
    client_id = input('Enter the app id (under the app name, next to "personal use script"): ')
    client_secret = input('Enter the app secret: ')
    username = input('Enter your Reddit username: ')

    # Collect subreddits
    subreddits = prompt_subreddits()
    
    return client_id, client_secret, username, subreddits

def prompt_subreddits():
    subreddits = []
    
    print('----- Subreddits')
    print("You can enter subreddit names or linkes, separated by commas, or enter one subreddit at a time")
    print("To stop, type '!q' or just press enter on an empty line")
    
    # Get subreddits
    while True:
        sub_input = input('Enter subreddit(s): ')
        
        if sub_input.lower() == '!q' or sub_input == '':
            break
        
        # Check if input has multiple subreddits
        if ',' in sub_input:
            subreddits.append([item.strip() for item in sub_input.split(',')])
        else:
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
    
    print('Subreddits to fetch from')
    for i in subreddits:
        print(f'\t- {i}')
        
    return subreddits
    
def prompt_llm():
    print('===== Groq Settings')
    
    groq_api = input('Please enter your Groq api key: ')
    model = input('Please enter the model you want to use: ')
    
    return groq_api, model
    

def prompt_elevenlabs():
    print('===== Elevenlabs Settings')
    
    elevenlabs_api = input('Please enter your elevenlabs api key: ')
    model_1 = input('Please enter the voice model id for host 1: ')
    model_2 = input('Please enter the voice model id for host 2: ')
    
    return elevenlabs_api, model_1, model_2 


def validate_settings(settings):
    pass

def validate_reddit(client_id, client_secret, username, subreddits):
    pass

def validate_llm(is_local, groq_api, model):
    pass

def validate_elevenlabs(elevenlabs_api, model_1, model_2):
    pass