import get_tweets
from string import punctuation

from nltk import pos_tag
from nltk import TweetTokenizer
from nltk import download
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples

corpora = ['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
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

    def __init__(self, text: list):
        # Text is passed as unclean data.
        self.text = text
        self.tokens = []
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))
        self.tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)

    def process_text(self) -> list[list[str]]:
    # this is unigram analysis
        
        for sentence in self.text:
            data = []
            # tokenize the sentence
            data = self.tokenizer.tokenize(sentence)

            # remove stopwords
            data = [token for token in data if token.isalpha() and token[0] not in self.stopwords]
            
            # POS tagging
            data = pos_tag(data)
            # not sure whether to put nouns in? - needed for semantic analysis
            TAGS = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'LS', 'MD', 'PDT', 
            'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']

            # lemmanize 
            data = [(self.lemmatizer.lemmatize(token),pos) for token,pos in data if pos not in TAGS]


            self.tokens.append(data)
        
        return self.tokens
    
class TrainModel:
    def __init__(self, text):
        self.text = text

    
tweet = twitter_samples.strings('positive_tweets.json')[:100]
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
