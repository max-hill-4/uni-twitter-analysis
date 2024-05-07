import requests
async def get_tweet(tweet:str):
    """
    Uses Twitter's Oemebed to return tweet data.
    Args:
        query (str) : The url of the tweet
    Returns:
        JSON: html data of the embeded tweet.
    """
    r = requests.get("https://publish.twitter.com/oembed?url=%s" % tweet)
    r = r.json()['html']
    return r 