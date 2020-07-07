"""Search tweets using tweepy"""
import os
from credentials import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
import json

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

search_words = "#wildfires"
date_since = "2018-11-16"

tweets = tweepy.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(5)

# Iterate and print tweets
for tweet in tweets:
    print(tweet._json)
    print("----")