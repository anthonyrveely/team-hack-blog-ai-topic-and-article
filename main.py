from flask import Flask, request, jsonify
import anthropic
import os
import ai_config

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

    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400

    # Process the transcript using Claude AI
    try:
        response = client.messages.create(
            model=ai_config.CLAUD_MODEL,
            max_tokens=1024,
            messages=[
                {
                    "role": "user", 
                    "content": f"Based on the following transcript, suggest 5 blog topics:\n\n{transcript}"
                }
            ]
        )
        blog_topics = response.content[0].text.split('\n')
        print(blog_topics)
    except Exception as e:
        return jsonify({'error': f'Error processing transcript: {str(e)}'}), 500

    result = {
        'received_transcript': transcript,
        'blog_topics': blog_topics
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)