import get_tweets

async def analyze_tweet(query):
    
    tweet = await get_tweets.get_tweet(query)
    
    NB = None
    NN = None
    data = (tweet, NB, NN)
    return {data}
