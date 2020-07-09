"""Common utility functions"""
from textblob import TextBlob
import re
import preprocessor as pre
import json
import logging
import wordninja

class Tweet:
    """Holds tweet object"""
    def __init__(self, text, id_str, created_at, sentiment):
        self.tweet = text
        self.id = id_str
        self.created_at = created_at
        self.sentiment = sentiment

    def get_tweet(self):
        return f"{self.id},{self.created_at},{self.sentiment},{self.tweet}"
        
    def __str__(self):
        return f"{self.id},{self.created_at},{self.sentiment},{self.tweet}"

    def __repr__(self):
        return json.dumps({
            "id":self.id,
            "created_at":self.created_at,
            "sentiment":self.sentiment,
            "tweet":self.tweet
        })

        
def preprocess(text):
    """Preprocess text"""
    
    # Decode in utf8
    text = text.encode('utf-8', 'replace').decode()

    # Remove HTML tags
    text = re.sub("<[^>]*>","",text)

    # Remove URLs and user mentions
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION)
    text = pre.clean(text)

    # Remove "#" character from hashtags(retaining hashtag content)
    text = re.sub("#"," ",text)

    # Get list of words, remove punctuation marks and convert ro lowercase
    text_blob = TextBlob(text)    
    text = text_blob.stripped.lower()
    
    return text
    
def calculate_sentiment(text):
    text_blob = TextBlob(text)
    polarity = text_blob.sentiment.polarity

    # 1-> positive
    # 0-> negative
    if polarity > 0:
        return 1
    return 0

def extract_tweet_features(tweet_dict):
    
    id_str = tweet_dict.get("id")
    created_at = tweet_dict.get("created_at")
    text= None
    try:
        text = preprocess(tweet_dict.get("full_text"))
    except Exception as e:
        logging.error(e)
        logging.error(tweet_dict.get("full_text"))
    sentiment = calculate_sentiment(text)

    # Creating tweet object
    tweet = Tweet(text, id_str, created_at, sentiment)
    return tweet

# sample = "@kim_siever Also, it's 🔔 obvious he doesn't give a sh-t about climatechange or denies it so this gives them the excuse to totally ignore it: even though Canada will differientially feels the effects of climate change more that lower latitude countries"
# print(preprocess(sample))