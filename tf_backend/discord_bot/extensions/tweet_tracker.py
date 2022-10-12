import os
from pytwitter import Api
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sid_obj = SentimentIntensityAnalyzer()

APP_KEY=os.environ['TWITTER_API_KEY']
APP_SECRET=os.environ['TWITTER_API_KEY_SECRET']
OAUTH_TOKEN=os.environ['ACCESS_TOKEN']
OAUTH_TOKEN_SECRET=os.environ['ACCESS_TOKEN_SECRET']
BEARER_TOKEN=os.environ['BEARER_TOKEN']
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET=os.environ['ACCESS_TOKEN_SECRET']

api = Api(bearer_token=BEARER_TOKEN)


def GetUserId(username):
    username = api.get_user(username=username)
    user_id = username.data.id

    return user_id

def GetName(username):
    username = api.get_user(username=username)
    name = username.data.name

    return name

def SearchTweets(kwarg):
    r = api.search_tweets(query=kwarg)
    count = 0
    total = 0
    for tweet in r.data:
        score = sid_obj.polarity_scores(tweet.text)
        total += score['compound']
        count += 1

    polarity = str(round(total/count,2))

    return polarity

def GetMentions(userID):
    r = api.get_mentions(user_id=userID)

    count = 0
    for mention in r.data:
        count += 1

    return "Not currently active"