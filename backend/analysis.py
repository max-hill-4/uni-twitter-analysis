import get_tweets

from string import punctuation
from random import shuffle

from nltk import pos_tag
from nltk import TweetTokenizer
from nltk import download
from nltk import NaiveBayesClassifier
from nltk import classify

from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples

from statistics import mean

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
# we could make a cool plot to prove under fitting and over fitting
class ProcessData:
    # make functions priva using _
    def __init__(self, text: list,  label: str = None):
        # Text is passed as unclean data.
        self.label = label
        self.text = text
        self.lemmatizer = WordNetLemmatizer()
        self.STOPWORDS = set(stopwords.words("english"))
        
        self.tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        
        self.TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }


    def convert_pos(self,tag: list):
                
        return self.TAGMAP.get(tag[0], 'n')
        

    def process_text(self) -> list[list[str]]:
        
        tokens = []
        for sentence in self.text:
            data = []
            # tokenize the sentence
            data = self.tokenizer.tokenize(sentence)

            # remove stopwords
            data = [token for token in data if token.isalpha() and token not in self.STOPWORDS]

            # Pull request needed for pos tag -> lemmas tag!
            data = pos_tag(data)
        
            # need to map pos tags to correct lemmatize tags!
            data = [self.lemmatizer.lemmatize(token, self.convert_pos(pos)) for token, pos in data]
            
            # this is maybe bad, becuase it means useless data is stored for unlabled data :(
            
            if data:
                tokens.append((data, self.label))
        
        return tokens
    
class TrainModel:

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def _calc_feature(self, tweet: list[str, str]) -> dict:
        
        # tweet is currently being passed with its label, but we dont need it.
        features = {}
        compound_scores = []
        positive_scores = []

        for word in tweet[0]:
            compound_scores.append(self.sia.polarity_scores(word)["compound"])
            positive_scores.append(self.sia.polarity_scores(word)["pos"])
        
        features['mean_compound'] = mean(compound_scores) 
        features['mean_positive'] = mean(positive_scores)

        return features


    def train(self, text):
       
        features = []
       
        for tweet in text:
            features.append((self._calc_feature(tweet), tweet[1]))

        classifier = NaiveBayesClassifier.train(labeled_featuresets=features)
        classifier.show_most_informative_features(5)

pos_tweet = twitter_samples.strings('positive_tweets.json')
neg_tweet = twitter_samples.strings('negative_tweets.json')

pos_data = ProcessData(pos_tweet, 'p').process_text()
neg_data = ProcessData(neg_tweet, 'n').process_text()

model = TrainModel().train(pos_data)














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
