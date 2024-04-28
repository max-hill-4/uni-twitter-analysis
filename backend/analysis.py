import get_tweets
import nltk

# Not happy with double parsing of query
def analyze_tweet(query):
    data = get_tweets.get_tweet(query)
    return data

def analyze_timeline(query):
    data = get_tweets.get_timeline(query)
    return data