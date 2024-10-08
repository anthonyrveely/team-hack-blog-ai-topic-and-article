from flask import Flask, request, jsonify
import anthropic
import os
import ai_config
import generate_blog_post as generate_blog_post

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(
    api_key=os.environ.get("CLAUDE_API_KEY")
)

@app.route('/transcript', methods=['POST'])
def process_transcript():
    data = request.json
    transcript = data.get('transcript')
    blog_topics = []
    products = []
    blog_posts = []

    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400

    # Process the transcript using Claude AI
    try:           
        response = client.messages.create(
            model=ai_config.CLAUDE_MODEL,
            max_tokens=4096,
            system=ai_config.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user", 
                    "content": f"Based on the following transcript, suggest blog topics and parse out the products discussed:\n\n{transcript}"
                }
            ],
            tools=[
                {
                    "name": "analyze_transcript_tool",
                    "description": "Use the given transcript to parse out all of the products discussed and generate blog topics for from the topics discussed in the transcript.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "blog_topics": {
                                "type": "array",
                                "description": "The blog topics to be generated from the transcript. max of 7 topics."
                            },
                            "products": {
                                "type": "array",
                                "description": "The products discussed in the transcript."
                            }
                        },
                        "required": ["blog_topics", "products"]
                    }
                }
            ],
            tool_choice={"type": "tool", "name": "analyze_transcript_tool"},
        )
        print("response")
        print(response.content)
        for content in response.content:
            if content.type == "tool_use":
                if content.name == "analyze_transcript_tool":
                    blog_topics.extend(content.input["blog_topics"])
                    products.extend(content.input["products"])
        
    except Exception as e:
        return jsonify({'error': f'Error processing transcript: {str(e)}'}), 500
    
    for blog_topic in blog_topics:
        blog_post = generate_blog_post.generate_blog_post_function(blog_topic, products)        
        blog_posts.append(blog_post)
        #wp_upload.upload_post(blog_topic, products)

    result = {
        'blog_topics': blog_topics,
        'products': products,
        'blog_post': blog_posts
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)