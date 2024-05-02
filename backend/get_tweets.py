import sentiment
import requests
from bs4 import BeautifulSoup


async def get_tweet(tweet):
    


    r = requests.get("https://publish.twitter.com/oembed?url=%s" % tweet)
    r = r.json()['html']


    soup = BeautifulSoup(r, 'html.parser')
    query = soup.find('blockquote').find('p').get_text(strip=True)

    sentiment_value = sentiment.Show_sentiment(query)
    result = {
    'html_content': r,
    'sentiment_value': sentiment_value
    }

    return (result)


async def get_timeline(tweet):

    oembed_url = f"https://publish.twitter.com/oembed?url={tweet}"
    r = requests.get(oembed_url)
    r = r.json()['html']

    soup = BeautifulSoup(r, 'html.parser')
    query = soup.find('blockquote').find('p').get_text(strip=True)
    sentiment_value = sentiment.Show_sentiment(query)
    #result = {
    #'html_content': r,
    #'sentiment_value': sentiment_value
    #}

    return (r)
