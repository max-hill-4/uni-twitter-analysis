import requests
from bs4 import BeautifulSoup
async def get_tweet(tweet:str):
    r = requests.get("https://publish.twitter.com/oembed?url=%s" % tweet)
    r = r.json()['html']
    return r 