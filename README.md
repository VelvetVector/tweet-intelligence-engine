This project is an AI-powered tool that helps users generate tweets and estimate how much engagement they might get. You simply enter details like company name and message, and the system creates a tweet and predicts the number of likes using a trained machine learning model.

The project combines multiple parts:

tweet_generator.py handles tweet creation using templates
like_predictor.pkl is the trained model for predicting likes
company_encoder.pkl and global_avg.pkl help the model understand company popularity
app.py brings everything together into an interactive Streamlit app

In simple terms, it takes an idea → turns it into a tweet → and tells you how well it might perform.
