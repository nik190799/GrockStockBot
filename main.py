import tweepy
import os

api_key = os.environ.get("X_API_KEY")
api_secret = os.environ.get("X_API_SECRET")
bearer_token = os.environ.get("X_BEARER_TOKEN")
access_token = os.environ.get("X_ACCESS_TOKEN")
access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

def api():
    # V2 Twitter API Authentication
    client = tweepy.Client(
        bearer_token,
        api_key,
        api_secret,
        access_token,
        access_token_secret,
        wait_on_rate_limit=True,
    )
    return client

def tweet(api, text: str):
    api.create_tweet(text=text)

if __name__ == '__main__':
    api = api()
    tweet(api, text = "Testing...")
