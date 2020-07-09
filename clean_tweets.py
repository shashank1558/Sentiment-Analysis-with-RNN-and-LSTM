"""Clean the raw tweets and store required features in csv"""
import json
from common import calculate_sentiment, preprocess, extract_tweet_features

input_file_name = "data/raw_tweets.txt"
output_file_name = "data/tweets.txt"

class Tweet:
    """Holds tweet object"""
    def __init__(self, text, id_str, created_at, sentiment):
        self.text = text
        self.id = id_str
        self.created_at = created_at
        self.sentiment = sentiment
   

if __name__ == "__main__":
    with open(input_file_name,"r",encoding='utf-8') as reader, open(output_file_name,"a") as writer:
        for tweet in reader:
            tweet_dict = json.loads(tweet)
            id_str, created_at, text, sentiment = extract_tweet_features(tweet_dict)
            print(text)
            break