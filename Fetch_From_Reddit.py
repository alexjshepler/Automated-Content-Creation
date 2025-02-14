import praw
import time
import prawcore
from tqdm import tqdm
from Database import insert_or_update_post, create_db
from Settings import load_settings

create_db()


def fetch_all_posts(settings):
    # Reddit app settings
    reddit = praw.Reddit(
        client_id=settings["reddit"]["client_id"],
        client_secret=settings["reddit"]["client_secret"],
        username=settings["reddit"]["username"],
        user_agent="RedditAppBot",
    )

    subreddits = settings["subreddits"]

    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    image_domains = ("i.redd.it", "imgur.com", "gfycat.com", "tenor.com", "giphy.com")

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)

        retries = 15
        attempt_num = 1
        last_post = None  # For pagination
        post_count = 0

        while True:  # Keep fetching until there are no more posts
            try:
                posts = subreddit.new(limit=100, params={"after": last_post})

                batch_count = 0

                for post in posts:
                    last_post = post.name  # Store the last post ID for pagination

                    # Skip image posts
                    if not post.is_self and (
                        post.url.endswith(image_extensions)
                        or any(domain in post.url for domain in image_domains)
                    ):
                        continue

                    author = post.author.name if post.author else "[deleted]"

                    post_data = {
                        "id": post.id,
                        "author": author,
                        "subreddit": sub,
                        "title": post.title,
                        "content": post.selftext if post.is_self else post.url,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "created_utc": post.created_utc,
                        "upvote_ratio": post.upvote_ratio,
                    }

                    insert_or_update_post(post_data)
                    post_count += 1
                    batch_count += 1

                if batch_count == 0:  # No more posts to fetch
                    print(f"Finished fetching all available posts from r/{sub}.")
                    break

                print(
                    f"Fetched {batch_count} more posts from r/{sub}, total: {post_count}"
                )

                time.sleep(2)  # Respect Reddit rate limits

            except prawcore.exceptions.RequestException as ex:
                print(
                    f"Reddit API request failed ({ex}). Retrying in {5 * attempt_num} seconds..."
                )
                time.sleep(5 * attempt_num)
                retries += 1

            except prawcore.exceptions.ServerError as ex:
                print(
                    f"Reddit server error ({ex}). Retrying in {10 * attempt_num} seconds..."
                )
                time.sleep(10 * attempt_num)
                retries += 1

            except Exception as ex:
                print(f"Unexpected error: {ex}")
                break
