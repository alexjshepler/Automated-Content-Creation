from Database import create_script_db, get_unused_posts, insert_script, set_has_script

from tqdm import tqdm

from ollama import ChatResponse, chat
from groq import Groq

IS_LOCAL = True

MODEL = 'llama4'

HOST_NAME_1 = 'Alex'
HOST_NAME_2 = 'Eric'

SYS_PROMPT = f"""You are a scriptwriter for a podcast called "Reddit Sagas". You create funny and engaging scripts between two hosts, {HOST_NAME_1} and {HOST_NAME_2}. The tone should be informal and funny, like two friends joking around and "shooting the shit".

Follow this structure strictly:
1. Podcast intro
2. One host introduces the post (author and title)
3. Full post is *read aloud by the hosts* (they take turns narrating or comment as it goes). Keep the post content intact, but interject naturally with reactions, jokes, or confusion.
4. Discussion after the post — must be fun, engaging, full of takes, jokes, analysis, and personal thoughts.
5. Wrap up with both hosts giving their final opinions and inviting the audience to chime in.

Use this format: "{HOST_NAME_1}: ..." and "{HOST_NAME_2}: ...". Do not include any stage directions, sound cues, or things like (laughs), (sighs), etc. All abbreviations should be written out fully. You are allowed to use light profanity.

The goal is to sound like real friends reading and reacting to a Reddit post together — not a stiff narration.

Here is the post to base the script on:
"""

USR_PROMPT = f"""
Generate a podcast script for the show "Reddit Sagas" based on the following flow:

1. Start with a funny, lighthearted intro by {HOST_NAME_1} and {HOST_NAME_2}.
2. One host introduces the post, including the Reddit author and title.
3. The hosts *read the full post together*, reacting as they go. They may take turns reading or interrupt each other to joke, question, or react. Make sure the full content of the post is still conveyed, but break it up naturally with realistic banter and short interjections. Expand acronyms like AITAH into full phrases.
4. After the post is read, the hosts dive into a humorous discussion. Include jokes, friendly disagreements, thoughtful analysis, and personal takes. Let each host’s personality shine — {HOST_NAME_1} is smarter and more logical; {HOST_NAME_2} is funnier, louder, and more emotional.
5. End with both giving their final verdict and asking listeners to share their own opinions.

{HOST_NAME_1} is smart, funny, college educated, likes to party, 21 years old, more mature than {HOST_NAME_2}, and takes the logical approach.
{HOST_NAME_2} is not as smart, funny, loves to party and drink, 21 years old, less mature than {HOST_NAME_1}, and takes the emotional approach.
"""

def generate_remote(post, client):
    pass

def generate_local(post):
    post_id = post[0]
    post_author = post[1]
    post_subreddit = post[2]
    post_title = post[3]
    post_content = post[4]

    response: ChatResponse = chat(model=MODEL, messages=[
        {
            'role':'system',
            'content': f'{SYS_PROMPT}\n{post_content}'
        },
        {
            'role':'user',
            'content':f'{USR_PROMPT}\nSubreddit: {post_subreddit}\nAuthor: {post_author}\nTitle: {post_title}\nContent: {post_content}'
        }
    ], stream=False)
    
    print(response['message']['content'])
    
    with open('script.txt', 'w') as file:
        file.write(response['message']['content'])

    # stream = chat(
    #     model=MODEL,
    #     messages=[
    #         {"role": "system", "content": SYS_PROMPT},
    #         {
    #             "role": "user",
    #             "content": f"{USR_PROMPT}\nSubreddit: {post_subreddit}\nAuthor: {post_author}\nTitle: {post_title}\nContent: {post_content}",
    #         },
    #     ],
    #     stream=True,
    # )
    
    # for chunk in stream:
    #     print(chunk['message']['content'], end='', flush=True)

def generate_scripts(settings):
    groq_settings = settings.get('groq', {})
    
    create_script_db()
    
    client = Groq(api_key=groq_settings.get('api_key'))
    
    posts = get_unused_posts()
    
    with tqdm(desc='Generating Scripts', total=len(posts), unit=' Scripts') as pbar:
        for post in posts:
            post_id = post[0]
            post_author = post[1]
            post_subreddit = post[2]
            post_title = post[3]
            post_content = post[4]
            
            if IS_LOCAL:
                output = generate_local(post)
            else:
                output = generate_remote(post, client)
                        
            script = {
                'id': post_id,
                'author': post_author,
                'subreddit': post_subreddit,
                'title': post_title,
                'content': post_content,
                'script': output
            }   
        
            # insert_script(script)
            # set_has_script(post_id)
            
            exit()
            pbar.update(1)
