from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media
import xmlrpc.client as xmlrpc_client
import requests

# WordPress site details
wp_url = os.getenv("WP_URL")
wp_username = os.getenv("EMAIL_ADDRESS")
wp_password = os.getenv("PASSWORD")

# Pixabay API details
pixabay_api_key = os.getenv("PIXABAY_API_KEY")

# Connect to the WordPress site
client = Client(wp_url, wp_username, wp_password)

def get_pixabay_image(query):
    url = f"https://pixabay.com/api/?key={pixabay_api_key}&q={query}&image_type=photo&per_page=3"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            image = data['hits'][0]  # Get the first image
            return image['largeImageURL'], image['tags']
    return None, None

def upload_post(title, content, image_query, tags=[], categories=[]):
    post = WordPressPost()
    post.title = title
    post.content = content

    # Get a relevant image based on the query
    image_url, image_tags = get_pixabay_image(image_query)
    if image_url:
        # Download the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            img_filename = f"pixabay_{image_query.replace(' ', '_')}.jpg"
            
            # Prepare image data for upload
            data = {
                'name': img_filename,
                'type': 'image/jpeg',
                'bits': xmlrpc_client.Binary(img_response.content)
            }

            # Upload the image to WordPress
            response = client.call(media.UploadFile(data))
            
            # Set as featured image
            post.thumbnail = response['id']

    post.terms_names = {
        'post_tag': tags + image_tags.split(', ') if image_tags else tags,
        'category': categories
    }
    post.post_status = 'publish'

    # Upload the post
    post_id = client.call(NewPost(post))

    print(f"Post uploaded successfully. Post ID: {post_id}")


#upload_post("Test Post", "This is a test post.", "Dog grooming")
