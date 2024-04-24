import requests
from bs4 import BeautifulSoup

async def get_tweet(tweet):
    """
    This is a request using Twitter's 
    """
    tweet = "https://twitter.com/taylorswift13/status/1781474914542756273?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Etweet"

    r = requests.get("https://publish.twitter.com/oembed?url=%s" % tweet)
    r = r.json()['html']
    
    soup = BeautifulSoup(r, 'html.parser')
    return (soup.find('blockquote').find('p').get_text(strip=True))
