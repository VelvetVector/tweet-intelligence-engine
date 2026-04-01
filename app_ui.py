import streamlit as st
import requests
from textblob import TextBlob
import datetime

st.set_page_config(page_title="AI Marketing Tool", layout="centered")

st.title("🚀 AI Content + Engagement Predictor")
st.write("Generate a tweet and predict its engagement!")

#inputs
company = st.text_input("Company Name", "Nike")

tweet_type = st.selectbox(
    "Tweet Type",
    ["announcement", "question", "general"]
)

message = st.text_input("Message", "launching new running shoes")
topic = st.text_input("Topic", "fitness")

has_media = st.checkbox("Include Media?", value=False)
hour = st.slider("Posting Hour (0–23)", 12, 0, 23)

#action
if st.button("🚀 Generate & Predict"):

    try:
        gen_res = requests.post(
            "http://127.0.0.1:5001/generate",
            json={
                "company": company,
                "tweet_type": tweet_type,
                "message": message,
                "topic": topic
            }
        ).json()

        tweet = gen_res["generated_tweet"]

        st.subheader("📝 Generated Tweet")
        st.success(tweet)

        word_count = len(tweet.split())
        char_count = len(tweet)
        sentiment = TextBlob(tweet).sentiment.polarity

        num_hashtags = tweet.count('#')
        num_mentions = tweet.count('@')

        avg_word_length = char_count / (word_count + 1)

        day_of_week = datetime.datetime.now().weekday()

        emoji_count = sum(1 for c in tweet if c in "😀😂😍🔥🎉🚀")

        company_post_count = 50

        #predict api call
        pred_res = requests.post(
            "http://127.0.0.1:5000/predict",
            json={
                "company": company,
                "word_count": word_count,
                "char_count": char_count,
                "sentiment": sentiment,
                "num_hashtags": num_hashtags,
                "num_mentions": num_mentions,
                "avg_word_length": avg_word_length,
                "has_media": int(has_media),
                "hour": hour,
                "day_of_week": day_of_week,
                "emoji_count": emoji_count,
                "company_post_count": company_post_count
            }
        ).json()

        #output
        st.subheader("📊 Predicted Likes")
        st.metric(label="Estimated Likes", value=pred_res["predicted_likes"])

    except Exception as e:
        st.error(f"Error: {e}")
