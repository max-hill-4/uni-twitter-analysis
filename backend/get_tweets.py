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
    text = """<blockquote class="twitter-tweet"><p lang="en" dir="ltr">When I was writing the Fortnight music video, I wanted to show you the worlds I saw in my head that served as the backdrop for making this music.  Pretty much everything in it is a metaphor or a reference to one corner of the album or another. For me, this video turned out to be… <a href="https://t.co/TLaUg9jEoo">pic.twitter.com/TLaUg9jEoo</a></p>&mdash; Taylor Swift (@taylorswift13) <a href="https://twitter.com/taylorswift13/status/1781474914542756273?ref_src=twsrc%5Etfw">April 20, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> """
    return (text)

# We would probably maybe have two gets, where one is ust for the embed code, 
# and the other for sentiment data! we would pass both ytohugh to jinja!