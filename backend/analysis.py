import get_tweets


async def analyze_tweet(query):
    
    data = await get_tweets.get_tweet(query)
    return {data }
