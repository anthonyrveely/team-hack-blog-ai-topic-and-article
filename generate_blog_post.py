import ai_config
import anthropic
import os
import dotenv

dotenv.load_dotenv()
def generate_blog_post_function(blog_topic: str, products: list):
    client = anthropic.Anthropic(
        api_key=os.environ.get("CLAUDE_API_KEY")
    )

    blog_post = {
        "blog_title": "",
        "blog_content": "",
        "tags": [],
        "categories": []
    }

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
            tools=[
                {
                    "name": "generate_blog_post_tool",
                    "description": "Use the given transcript to parse out all of the products discussed and generate blog topics for from the topics discussed in the transcript.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "blog_title": {
                                "type": "string",
                                "description": "The blog title to be generated from the transcript."
                            },
                            "blog_content": {
                                "type": "string",
                                "description": "The blog content to be generated from the transcript."
                            },
                            "tags": {
                                "type": "array",
                                "description": "The products discussed in the transcript."
                            },
                            "categories": {
                                "type": "string",
                                "description": "The categories of the blog post."
                            }
                        },
                        "required": ["blog_title", "blog_content", "tags", "categories"]
                    }
                }
            ],
            tool_choice={"type": "tool", "name": "generate_blog_post_tool"}
        )

        print("response")
        print(response.content)

        for content in response.content:
            if content.type == "tool_use":
                if content.name == "generate_blog_post_tool":
                    blog_post["blog_title"] = content.input["blog_title"]
                    blog_post["blog_content"] = content.input["blog_content"]
                    blog_post["tags"] = content.input["tags"]
                    blog_post["categories"] = content.input["categories"]
        
        print(blog_post)
        return blog_post
    
    except Exception as e:
        print(e)
        return None
    
    