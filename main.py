import praw
import json


def load_settings():
    """Load settings from a JSON file or prompt the user to create one."""
    settings = {}

    try:
        # Try to load settings from the JSON file
        with open("settings.json", "r") as f:
            settings = json.load(f)
        print("\nSettings loaded successfully!\n")
    except FileNotFoundError:
        print("\nSettings file not found. Let's create one!\n")

    # If settings are not available, prompt the user to create new ones
    if not settings:
        settings = prompt_user_for_settings()

    # Validate settings
    settings = validate_settings(settings)

    # Save the settings to the JSON file
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

    return settings


def prompt_user_for_settings():
    """Prompt the user to enter settings and create the settings JSON."""
    print("\n--- Reddit App Setup ---")
    print("First, go to: https://www.reddit.com/prefs/apps\n")

    # Ask if the user has an app created on Reddit
    while True:
        has_app = input(
            "Do you have an app made on Reddit? If not, enter 'n' (y/n): "
        ).lower()
        if has_app in ["y", "n"]:
            break
        else:
            print("Please enter 'y' or 'n'.")

    if has_app == "n":
        print("\nLet's create one! Follow these steps:")
        print(
            """
        1) Go to 'are you a developer? Create an app...'
        2) Enter any name for your app, select 'script', and use any valid redirect URI (e.g., https://google.com).
        3) Complete the captcha and click 'Create app'.
        4) Once created, click 'edit app' to see your app details.
        """
        )

    # Collect user inputs for the app details
    print("\n--- App Details ---")
    client_id = input(
        'Enter the app id (under the app name, next to "personal use script"): '
    )
    client_secret = input("Enter the app secret: ")
    username = input("Enter your Reddit username: ")

    # Collect user preferences for the subreddits
    subreddits = prompt_for_subreddits()

    # Collect user preference for fetch method
    fetch_methods = ["top", "hot", "new", "controversial", "rising"]
    print("\n--- Fetch Method ---")
    while True:
        fetch_method = input(
            f"How do you want to fetch posts? ({', '.join(fetch_methods)}): "
        ).lower()
        if fetch_method in fetch_methods:
            break
        else:
            print(f"Invalid choice. Please choose one of {', '.join(fetch_methods)}.")

    # Collect user preference for limit
    print("\n--- Post Limit ---")
    while True:
        try:
            limit = int(input("Enter the number of posts to fetch: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    # Return settings dictionary
    return {
        "reddit": {
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
        },
        "subreddits": subreddits,
        "fetch_method": fetch_method,
        "limit": limit,
    }


def prompt_for_subreddits():
    """Prompt the user to enter subreddits, either separated by commas or one at a time."""
    subreddits = []
    print("\n--- Subreddit Preferences ---")
    print(
        "You can enter subreddit names or links, separated by commas, or enter one subreddit at a time."
    )
    print("To stop, type '!quit'.")

    while True:
        # Ask user to input subreddits either separated by commas or one at a time
        sub_input = input("Enter subreddit(s): ")

        if sub_input.lower() == "!quit":
            break

        # Check if input contains commas (multiple subreddits)
        if "," in sub_input:
            subreddits.extend([item.strip() for item in sub_input.split(",")])
        else:
            subreddits.append(sub_input.strip())

    # Normalize subreddits to strip "r/" if entered as a link (e.g., "https://reddit.com/r/subreddit_name")
    subreddits = [
        sub.replace("https://reddit.com/r/", "").replace("r/", "").strip()
        for sub in subreddits
    ]

    print(f"Subreddits to fetch: {subreddits}")
    return subreddits


def validate_settings(settings):
    """Validate the entered settings and prompt user to re-enter any invalid or missing settings."""
    print("\n--- Validating Settings ---")

    # Check if Reddit settings are missing or empty
    if (
        not settings.get("reddit")
        or not settings["reddit"].get("client_id")
        or not settings["reddit"].get("client_secret")
        or not settings["reddit"].get("username")
    ):
        print(
            "Error: Reddit app credentials are missing or incomplete. Please re-enter them."
        )
        settings = prompt_user_for_settings()

    # Check if subreddits are missing or empty
    if not settings.get("subreddits") or not settings["subreddits"]:
        print("Error: No subreddits specified. Please re-enter them.")
        settings["subreddits"] = prompt_for_subreddits()

    # Validate fetch method
    fetch_methods = ["top", "hot", "new", "controversial", "rising"]
    if settings.get("fetch_method") not in fetch_methods:
        print(
            f"Error: Invalid fetch method. Must be one of {', '.join(fetch_methods)}. Please re-enter it."
        )
        settings["fetch_method"] = input(
            f"How do you want to fetch posts? ({', '.join(fetch_methods)}): "
        ).lower()

    # Validate limit
    if not isinstance(settings.get("limit"), int) or settings.get("limit") <= 0:
        print("Error: Invalid limit. Please enter a valid number greater than 0.")
        while True:
            try:
                settings["limit"] = int(input("Enter the number of posts to fetch: "))
                if settings["limit"] > 0:
                    break
                else:
                    print("The number must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")

    print("Settings validated successfully!\n")
    return settings


def main():
    print("\n--- Reddit Settings Configuration ---")
    settings = load_settings()


if __name__ == "__main__":
    main()
