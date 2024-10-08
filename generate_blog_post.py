import ai_config
import anthropic
import os
import dotenv

dotenv.load_dotenv()
def generate_blog_post_function(blog_topic: str, products: list):
    client = anthropic.Anthropic(
        api_key=os.environ.get("CLAUDE_API_KEY")
    )
    try:           
        response = client.messages.create(
            model=ai_config.CLAUDE_MODEL,
            max_tokens=4096,
            system=ai_config.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user", 
                    "content": f"Please create a 500 word blog post for this topic and highlight and create a backlink to the relevant products related to the blog post:\n\n<blog_topic>{blog_topic}</blog_topic><products>{products}</products>"
                }
            ],
        )
        
        print(response.content)
        return response.content[0].text
    
    except Exception as e:
        print(e)
        return None
    
    