import praw
import emoji
import re

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id="HJG70Y4rZ6SGk1F9unEY8g",
    client_secret="qFq5gT2tNjMfyHsX4aFNqNnXKKetnA",
    user_agent="YOUR_USER_AGENT",
    username='ExistingPain9212',
    password='Mudar!@#12'
)

# Subreddit to monitor
SUBREDDIT_NAME = "letters"

def remove_emojis(text):
    # Remove emojis, punctuation, and spaces
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return ''.join(text.split())

def get_and_compare_posts():
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    posts = list(subreddit.new(limit=1000))  # Get the ten newest posts
    
    newest_post = posts[0]
    cleaned_newest = remove_emojis(newest_post.selftext)
    
    # Compare with posts 2 through 1000
    for i, post in enumerate(posts[1:1000], 2):
        cleaned_post = remove_emojis(post.selftext)
        
        if cleaned_newest == cleaned_post:
            print(f"\nYES - The newest post matches post #{i}!")
            # Remove the newest post and add moderator comment
            newest_post.mod.remove()
            newest_post.mod.send_removal_message(
                message="This post has been removed as it is a duplicate of an existing post.",
                type="public"
            )
            return  # Stop comparing if match is found
        else:
            print(f"\nNO - The newest post does not match post #{i}")

if __name__ == "__main__":
    get_and_compare_posts()


