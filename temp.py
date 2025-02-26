from ollama import chat

from Database import get_random_AITAH_post

<<<<<<< HEAD
MODEL = "llama3.2"
PROMPT = 'Generate a podcast script where two hosts, Alex and Jamie, introduce the show and themselves, then one host reads the following Reddit post in a natural storytelling style. After reading, they discuss the story, analyzing different viewpoints, debating who is in the wrong, and adding humor, friendly banter, and a mix of logical and emotional reasoning. The conversation should feel engaging and informal, like two friends chatting. Finally, they summarize their opinions and invite listeners to share their thoughts. I only want the script, it should be formatted by "Author: " then their responses. Here is the post information: '
=======
MODEL = "llama3.3"
PROMPT = "Generate a podcast script. The podcast is called \"Reddit Sagas\". The flow of the podcast is as follows: Introduce the podcast, read the post, then have a discussion about the post. There are two hosts of the podcast. Alex who is a male, 21 years old, college educated, and the more mature one. And Eric, a male, 21 years old, a frat guy, in college, and is the less mature one who is also less intelligent. The hosts introduce themselves and the podcast. One of the hosts introduces the post, gives the author of the post, and then title of the post. The hosts do not give a summary of the post before reading it. Then one of the hosts reads the post in its entirety. While the post is being read either host is allowed to interject but rarely. The other host doesn\'t have to respond, if the other host does respond this could lead into a small discussion about whats been coverd so far in the post, it could go into a rant, or the hosts could go offtopic for a little bit, but they get back on track quickly and continue reading the post from where they left off. After reading, the hosts will discuss the story, analyzing different viewpoints, debating who is in the wrong, and adding humor, friendly banter, personal sotries, and a mix of logical and emotional reasoning. The conversation should feel engaging and informal, like two friends chatting. At the end, the hosts should summarize their opinions and invite listeners to share their throughs. Whenever there are accronyms the hosts should say the full words and not the letters (for example if there is \"AITAH\" in the post the host should read \"Am i the ass hole\"). The script should be formatted as \"Alex: ...\", \"Eric: ...\" to signify the host that is speaking. You should only generate the script and nothing else. Here is the post information: "
>>>>>>> 99775e983cb55c6809797ceaff95a0ed9a456d66

post = get_random_AITAH_post()

while len(post[4].split(' ')) <= 100 or len(post[4].split(' ')) >= 400:
    post = get_random_AITAH_post()

post_title = post[3]
post_content = post[4]
post_author = post[1]

print(
    f"Post:\n\tAuthor: {post_author}\n\tTitle: {post_title}\n\tContent: {post_content}\n\tWord Count: {len(post_content.split(' '))}\n\nScript:\n"
)

stream = chat(
    model='llama3.3',
    messages=[{'role': 'user', 'content': f'{PROMPT} [Post Title: {post_title} | Post Author: {post_author} | Post Content: {post_content}]'}],
    stream=True,
    )

with open('output_test.txt', 'w') as file:
    for chunk in stream:
        curr_chunk = chunk["message"]["content"]
        print(curr_chunk, end="", flush=True)
        file.write(curr_chunk)
