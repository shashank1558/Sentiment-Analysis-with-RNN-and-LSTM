"""Common utility functions"""
from textblob import TextBlob

def preprocess(text):
    tweet_blob = TextBlob(text)
    print(tweet_blob.words)
    return text
    
def calculate_sentiment(text):
    pass

def extract_tweet_features(tweet_dict):
    id_str = tweet_dict.get("id")
    created_at = tweet_dict.get("id")
    text = preprocess(tweet_dict.get("full_text"))
    sentiment = calculate_sentiment(text)