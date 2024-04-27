import get_tweets
from string import punctuation


from nltk import TweetTokenizer
from nltk import download
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples

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

class ProcessData:

    def __init__(self, text):
        # Text is passed as unclean data.
        self.text = text
        self.tokens = []
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))
        self.tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)

    def process_text(self) -> list[str]:
        # tokenize the sentence
        self.tokens = self.tokenizer.tokenize(self.text)
        # remove stopwords
        self.tokens = [token for token in self.tokens if token.isalpha() and token not in self.stopwords]
        # lemmanize
        self.tokens = [self.lemmatizer.lemmatize(token) for token in self.tokens]
        return self.tokens
    

tweet = twitter_samples.strings()[10]
a = ProcessData(tweet)
new_tokens = a.process_text()
print(new_tokens)




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
