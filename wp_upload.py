from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# WordPress site details
wp_url = os.getenv("WP_URL")
wp_username = os.getenv("EMAIL_ADDRESS")
wp_password = os.getenv("PASSWORD")

# Connect to the WordPress site
client = Client(wp_url, wp_username, wp_password)

def upload_post(title, content, tags=[], categories=[]):
    # Create a new post
    post = WordPressPost()
    post.title = title
    post.content = content
    post.terms_names = {
        'post_tag': tags, # format: ['tag1', 'tag2'],
        'category': categories #['category1', 'category2']
    }
    post.post_status = 'publish'  # Or 'draft' if you don't want to publish immediately

    # Upload the post
    post_id = client.call(NewPost(post))

    print(f"Post uploaded successfully. Post ID: {post_id}")


#upload_post("Test Post", "This is a test post.")
