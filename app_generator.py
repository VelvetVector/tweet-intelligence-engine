from flask import Flask, request, jsonify
from tweet_generator import SimpleTweetGenerator

app = Flask(__name__)
generator = SimpleTweetGenerator()

@app.route('/')
def home():
    return "Tweet Generator API running 🚀"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()

        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')
        topic = data.get('topic', 'innovation')

        tweet = generator.generate_tweet(company, tweet_type, message, topic)

        return jsonify({
            'generated_tweet': tweet,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)