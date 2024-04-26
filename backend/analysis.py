import get_tweets
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples

# These are needed! - dont want to run checks everytime
#from nltk import download
#download('vader_lexicon')
#download('twitter_samples')

"""
Designing my own model: 

-> Tokenize all of the text
-> Remove Stop Words ( I, Me, And )
-> Lemmatization - ( Group words, run running)
-> POS tagging improves Lemmatization alot, Nouns are not Sentiment!
-> Choose important text and create numerical representation
-> Run classification models

"""
async def analyze_tweet(query):
    
    # This is the built in vader ML model from nltk!
    data = await get_tweets.get_tweet(query)
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(data)["compound"]
    return {data : score}
