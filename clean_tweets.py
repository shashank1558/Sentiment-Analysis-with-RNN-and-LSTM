"""Clean the raw tweets and store required features in csv"""
import json
import csv
from common import calculate_sentiment, preprocess, extract_tweet_features

input_file_name = "data/raw_tweets.txt"
output_file_name = "data/tweets.csv"

if __name__ == "__main__":
    with open(input_file_name,"r",encoding='utf-8') as reader, open(output_file_name,"a", encoding="utf-8") as writer:
        writer.write("id,created_at,sentiment,tweet")
        count = 0
        for tweet in reader:
            tweet_dict = json.loads(tweet)
            tweet_object = extract_tweet_features(tweet_dict)
            writer.write("\n")
            writer.write(tweet_object.get_tweet())
            count +=1
            if count % 1000==0:
                print(count)