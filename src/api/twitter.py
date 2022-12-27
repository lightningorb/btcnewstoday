import tweepy
from bn_secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)


def get_tweet(tweet_id):
    tweet = client.get_tweet(id=tweet_id)
    return tweet[0].text


def send_dm(user_id, text):
    api.send_direct_message(user_id, text)


def get_user_id(username):
    user = client.get_user(username=username)
    return user.data.id
