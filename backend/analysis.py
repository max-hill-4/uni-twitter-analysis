import get_tweets
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

# These are needed! - dont want to run checks everytime
#from nltk import download
#download('vader_lexicon')
#download('twitter_samples')

# Not happy with double parsing of query

async def analyze_tweet(query):
    data = await get_tweets.get_tweet(query)
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(data)["compound"]
    return {data : score}
