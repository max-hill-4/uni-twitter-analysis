import get_tweets as gt

# Sentiment analysis

# Not happy with double parsing of query
def analysis_tweet(query):
    # data will be the tweet data
    data = gt.get_tweet(query)
    # ML will be the sentiment analysis

    return data