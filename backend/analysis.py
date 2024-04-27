import get_tweets
from string import punctuation

from nltk import corpus
from nltk import TweetTokenizer
from nltk import download
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer


corpora = ['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet']
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

class Anaylsis():

    def lemmenizer(self, tokens) -> list[str]:
        l = WordNetLemmatizer()
        new_tokens = []

        for token in tokens:
            new_tokens.append(l.lemmatize(token))

        return new_tokens

    def clean_tokens(self, tokens) -> list[str]:

        stopwords = corpus.stopwords.words("english")
        
        new_tokens = []
        for token in tokens:
            if token not in stopwords and token.isalpha():
                new_tokens.append(token)
            
        return new_tokens

    def tokenize(self, tweet) -> list[str]:
        
        tokenizer = TweetTokenizer(
            preserve_case=False,
            strip_handles=True,
            reduce_len=True)

        return tokenizer.tokenize(tweet)

tweet = corpus.twitter_samples.strings()[10]
a = Anaylsis()
tokens = a.tokenize(tweet)
tokens = a.clean_tokens(tokens)
print(a.lemmenizer(tokens))




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
