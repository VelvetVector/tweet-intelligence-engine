from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# ===============================
# 🔹 Load model + encoders
# ===============================
model = joblib.load('like_predictor.pkl')
company_encoder = joblib.load('company_encoder.pkl')
global_avg = joblib.load('global_avg.pkl')

# ===============================
# 🔹 Routes
# ===============================
@app.route('/')
def home():
    return "API is working 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # 🔹 Extract company
        company = data['company']

        # 🔹 Encode company
        company_target_enc = company_encoder.get(company, global_avg)

        # 🔹 Build feature array (ORDER MATTERS)
        features = np.array([
            data['word_count'],
            data['char_count'],
            data['sentiment'],
            data['num_hashtags'],
            data['num_mentions'],
            data['avg_word_length'],
            data['has_media'],
            data['hour'],
            data['day_of_week'],
            data['emoji_count'],
            data['company_post_count'],
            company_target_enc
        ]).reshape(1, -1)

        # 🔹 Predict
        prediction = model.predict(features)[0]

        return jsonify({
            'predicted_likes': int(np.expm1(prediction))  # convert back from log
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

# ===============================
# 🔹 Run app
# ===============================
if __name__ == '__main__':
    app.run(debug=True)