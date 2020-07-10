"""Search tweets using tweepy"""
import osdeactivate
from credentials import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
import json

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

search_words = "love"
date_since = "2018-11-16"


if __name__ == "__main__":
    tweets= None
    try:
        tweets = tweepy.Cursor(api.search,
                    q=search_words, count=100,
                    lang="en",tweet_mode="extended",
                    since=date_since).items(20000)
    except Exception as e:
            print("!!!! --- "+str(e))

    # with open("data/raw_tweets.txt","a") as file:
    #     for tweet in tweets:
    #         file.write(json.dumps(tweet._json))
    #         file.write("\n")
