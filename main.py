from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transcript', methods=['POST'])
def process_transcript():
    data = request.json
    transcript = data.get('transcript')

    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400

    # Process the transcript here
    # For now, we'll just return it as-is
    result = {'received_transcript': transcript}

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)