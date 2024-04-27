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
-> Feature Selection
    Tag the data with our 'feature data' - (Frequency, VADER score , etc.)
    Tag the data with if it is meant to be positive or negative

-> Train classification models

-> Compare the classification models

TD? 
-> are we going to create an entire model everytime i load the program? 
-> could i create the model and use an api to call to it? 

"""
async def analyze_tweet(query):
    
    # This is the built in vader ML model from nltk!
    data = await get_tweets.get_tweet(query)
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(data)["compound"]
    return {data : score}
