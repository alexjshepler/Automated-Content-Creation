import ollama

from Database import get_random_AITAH_post

MODEL = "llama3.2"
PROMPT = 'Generate a podcast script where two hosts, Alex and Jamie, introduce the show and themselves, then one host reads the following Reddit post in a natural storytelling style. After reading, they discuss the story, analyzing different viewpoints, debating who is in the wrong, and adding humor, friendly banter, and a mix of logical and emotional reasoning. The conversation should feel engaging and informal, like two friends chatting. Finally, they summarize their opinions and invite listeners to share their thoughts. I only want the script, it should be formatted by "Author: " then their responses. Here is the post information: '

post = get_random_AITAH_post()

post_title = post[3]
post_content = post[4]
post_author = post[1]

print(
    f"Post:\n\tAuthor: {post_author}\n\tTitle: {post_title}\n\tContent: {post_content}"
)

response = ollama.generate(
    model=MODEL,
    prompt=f"{PROMPT} | post title: {post_title} | post content: {post_content} | post author: {post_author}",
)

print(response["response"])

with open('Test.txt', 'w') as file:
    file.write(response['response'])