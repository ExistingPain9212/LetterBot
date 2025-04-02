import praw
import emoji
import re
from Levenshtein import ratio

# Reddit API credentials
reddit = praw.Reddit(
    client_id="HJG70Y4rZ6SGk1F9unEY8g",
    client_secret="qFq5gT2tNjMfyHsX4aFNqNnXKKetnA",
    user_agent="YOUR_USER_AGENT",
    username='ExistingPain9212',
    password='Mudar!@#12'
)

# Subreddit to monitor
SUBREDDIT_NAME = "letters"
SIMILARITY_THRESHOLD = 0.90  # 90% similarity threshold

def remove_emojis(text):
    # Remove emojis, punctuation, and spaces
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return ' '.join(text.split())  # Keep spaces between words for better comparison

def calculate_similarity(text1, text2):
    # Calculate similarity ratio using Levenshtein distance
    return ratio(text1.lower(), text2.lower())

def get_and_compare_posts():
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    posts = list(subreddit.new(limit=1000))
    
    newest_post = posts[0]
    cleaned_newest = remove_emojis(newest_post.selftext)
    
    # Compare with posts 2 through 1000
    for i, post in enumerate(posts[1:1000], 2):
        cleaned_post = remove_emojis(post.selftext)
        
        similarity = calculate_similarity(cleaned_newest, cleaned_post)
        
        if similarity >= SIMILARITY_THRESHOLD:
            print(f"\nYES - The newest post matches post #{i} with {similarity:.2%} similarity!")
            # Remove the newest post, add moderator comment with link, and lock it
            matching_post_url = f"https://reddit.com{post.permalink}"
            newest_post.mod.remove()
            newest_post.mod.send_removal_message(
                message=f"This post has been removed as it is {similarity:.1%} similar to an existing post.\n\nOriginal post: {matching_post_url}",
                type="public"
            )
            newest_post.mod.lock()
            return  # Stop comparing if match is found
        else:
            print(f"\nNO - The newest post does not match post #{i} (similarity: {similarity:.2%})")

if __name__ == "__main__":
    get_and_compare_posts()


