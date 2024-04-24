import get_tweets as gt

# Sentiment analysis

# Not happy with double parsing of query
def analysis_tweet(query):
    data = gt.get_tweet(query)

    return data