import get_tweets


# Not happy with double parsing of query
def analyze_tweet(query):
    data = get_tweets.get_tweet(query)
    return data