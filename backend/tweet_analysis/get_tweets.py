# Webscraping for tweets
# Data cleaning

import requests
from bs4 import BeautifulSoup

async def get_tweet(tweet):
    """
    This is a request using Twitter's 
    """
    r = requests.get(f'https://publish.twitter.com/oembed?url={tweet}')
    r = r.json()['html']

    soup = BeautifulSoup(r, 'html.parser')
    return (soup.find('blockquote').find('p').get_text(strip=True))
