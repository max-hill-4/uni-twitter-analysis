import requests

async def get_tweet(tweet):
    r = requests.get("https://publish.twitter.com/oembed?url=%s" % tweet)
    r = r.json()['html']
    return (r)
