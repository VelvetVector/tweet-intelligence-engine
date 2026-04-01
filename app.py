import streamlit as st
import joblib
import numpy as np
from textblob import TextBlob
import datetime
from tweet_generator import SimpleTweetGenerator

# ===============================
# 🔹 Load model + encoder
# ===============================
@st.cache_resource
def load_model():
    return joblib.load("like_predictor.pkl")

@st.cache_resource
def load_encoder():
    return joblib.load("company_encoder.pkl")

@st.cache_resource
def load_global_avg():
    return joblib.load("global_avg.pkl")

@st.cache_resource
def load_generator():
    return SimpleTweetGenerator()

model = load_model()
company_encoder = load_encoder()
global_avg = load_global_avg()
generator = load_generator()

# ===============================
# 🔹 UI
# ===============================
st.title("🚀 Tweet Intelligence Engine")
st.write("Generate tweets and predict engagement!")

company = st.text_input("Company Name", "Nike")

tweet_type = st.selectbox(
    "Tweet Type",
    ["announcement", "question", "general"]
)

message = st.text_input("Message", "launching new running shoes")

has_media = st.checkbox("Include Media?", value=False)
hour = st.slider("Posting Hour", 0, 23, 12)

# ===============================
# 🔹 BUTTON
# ===============================
if st.button("🚀 Generate & Predict"):

    # 🔹 Generate tweet
    tweet = generator.generate_tweet(company, tweet_type, message)

    st.subheader("📝 Generated Tweet")
    st.success(tweet)

    # ===============================
    # 🔹 Feature Engineering
    # ===============================
    word_count = len(tweet.split())
    char_count = len(tweet)
    sentiment = TextBlob(tweet).sentiment.polarity

    num_hashtags = tweet.count('#')
    num_mentions = tweet.count('@')

    avg_word_length = char_count / (word_count + 1)

    day_of_week = datetime.datetime.now().weekday()

    emoji_count = sum(1 for c in tweet if c in "😀😂😍🔥🎉🚀")

    company_post_count = 50  # placeholder

    company_target_enc = company_encoder.get(company, global_avg)

    # ===============================
    # 🔹 Prediction
    # ===============================
    features = np.array([[
        word_count,
        char_count,
        sentiment,
        num_hashtags,
        num_mentions,
        avg_word_length,
        int(has_media),
        hour,
        day_of_week,
        emoji_count,
        company_post_count,
        company_target_enc
    ]])

    pred = model.predict(features)[0]
    predicted_likes = int(np.expm1(pred))

    # ===============================
    # 🔹 Output
    # ===============================
    st.subheader("📊 Predicted Likes")
    st.metric("Estimated Likes", predicted_likes)