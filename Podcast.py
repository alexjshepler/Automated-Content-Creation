from tqdm import tqdm
from ollama import generate

from Database import get_all_AITAH_posts, is_post_in_podcast_db, create_podcast_db, insert_script


MODEL = "llama3.3"
PROMPT = 'Generate a podcast script. The podcast is called "Reddit Sagas". The flow of the podcast is as follows: Introduce the podcast, read the post, then have a discussion about the post. There are two hosts of the podcast. Alex who is a male, 21 years old, college educated, and the more mature one. And Eric, a male, 21 years old, a frat guy, in college, and is the less mature one who is also less intelligent. The hosts introduce themselves and the podcast. One of the hosts introduces the post, gives the author of the post, and then title of the post. The hosts do not give a summary of the post before reading it. Then one of the hosts reads the post in its entirety. While the post is being read either host is allowed to interject but rarely. The other host doesn\'t have to respond, if the other host does respond this could lead into a small discussion about whats been coverd so far in the post, it could go into a rant, or the hosts could go offtopic for a little bit, but they get back on track quickly and continue reading the post from where they left off. After reading, the hosts will discuss the story, analyzing different viewpoints, debating who is in the wrong, and adding humor, friendly banter, personal sotries, and a mix of logical and emotional reasoning. The conversation should feel engaging and informal, like two friends chatting. At the end, the hosts should summarize their opinions and invite listeners to share their throughs. Whenever there are accronyms the hosts should say the full words and not the letters (for example if there is "AITAH" in the post the host should read "Am i the ass hole"). There should be no breaks like for ads or whatever else. The script should be formatted as "Alex: ...", "Eric: ..." to signify the host that is speaking. You should only generate the script and nothing else. Here is the post information: '

def generate_scripts():
    create_podcast_db()

    posts = get_all_AITAH_posts()

    with tqdm(desc='Generating Scripts', total=len(posts), unit=' Script') as pbar:
        for post in posts:
            if is_post_in_podcast_db(post[4]):
                continue

            post_id = post[0]
            post_author = post[1]
            post_subreddit = post[2]
            post_title = post[3]
            post_content = post[4]
            
            response = generate(model=MODEL, prompt=f'{PROMPT} [Post Title: {post_title} | Post Content: {post_content} | Post Author: {post_author}]')
            
            insert_script(post_id, post_subreddit, post_author, post_title, post_content, response['response'])
            
            pbar.update(1)


generate_scripts()

def generate_audio():
    pass