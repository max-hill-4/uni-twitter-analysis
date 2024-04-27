import get_tweets
from string import punctuation
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import corpus
from nltk import TweetTokenizer
from nltk import download

corpora = ['vader_lexicon', 'twitter_samples', 'stopwords']
# Need to find way to check if already installed
for i in corpora:
     download(i)

"""
Designing my own model: 

-> Tokenize all of the text
-> Remove Stop Words ( I, Me, And )
-> Lemmatization - ( Group words, run running)
-> POS tagging improves Lemmatization alot, Nouns are not Sentiment!
-> Feature Selection
    Tag the data with our 'feature data' - (Frequency, VADER score , etc.)
    Tag the data with the positive or negative 'actual' data

-> Train classification models

-> Compare the classification models

TD? 
-> are we going to train a entire model using a classifier everytime I load the program? 
-> could i create train model and use an api to call to it? 

https://necromuralist.github.io/Neurotic-Networking/posts/nlp/01-twitter-preprocessing-with-nltk/index.html
"""
def clean_tokens(tokens) -> list[str]:

    stopwords = corpus.stopwords.words("english")
    
    clean_tokens = []
    for token in tokens:
        if token not in stopwords and token.isalpha():
            clean_tokens.append(token)
        
    return clean_tokens

def tokenize(tweet) -> list[str]:
    
    tokenizer = TweetTokenizer(
        preserve_case=False,
        strip_handles=True,
        reduce_len=True)

    return tokenizer.tokenize(tweet)

tweet = corpus.twitter_samples.strings()[10]
tokens = tokenize(tweet)
print(clean_tokens(tokens))




async def analyze_tweet(query):
    """
    Get the data using get_tweets.
    get predicted score from classifier.
    """
    

    # This is the built in vader ML model from nltk!
    data = await get_tweets.get_tweet(query)
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(data)["compound"]
    return {data : score}
