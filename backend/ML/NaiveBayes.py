from .model import Model

from nltk import pos_tag
from nltk import NaiveBayesClassifier
from nltk import classify
from nltk import TweetTokenizer

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from random import shuffle
from statistics import mean

import joblib

class NaiveBayes(Model):
    def __init__(self) -> None:
        super().__init__()
        # TD: should try to make stopwords static, and data needed for objects static also.
        self.sia = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()

        self.tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        
        self.TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }

        self.STOPWORDS = set(stopwords.words("english"))
        
        sia = SentimentIntensityAnalyzer()
    
    def _preprocess(self, tweet):

        data = self.tokenizer.tokenize(tweet)

        data = [token for token in data if token.isalpha() and token not in self.STOPWORDS]

        # (low) TD: Pull request pos tag (tagset) to work with lemmatize
        data = pos_tag(data)
    
        # (low) TD: refact if data + lemmatize + pos_tag
        
        data = [self.lemmatizer.lemmatize(token, self.TAGMAP.get(pos, 'n')) for token, pos in data]
        
        return data
    
    def _features(self, tweet):

        data = self._preprocess(tweet)
        if not data:
            return {}

        features = {}
        positive_scores = []
        compound_scores = []

        for word in data:
            positive_scores.append(self.sia.polarity_scores(word)["pos"])
            compound_scores.append(self.sia.polarity_scores(word)["compound"])
        features['pos_score'] = mean(positive_scores)
        features['comp_score'] = mean(compound_scores)
        return features
    
    def _trainmodel(self):

        features = []
        for tweet in self.pos_data:
            features.append((self._features(tweet), 'p'))

        for tweet in self.neg_data:
            features.append((self._features(tweet), 'n'))

        shuffle(features)
        classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:1500])
        joblib.dump(classifier, r'backend\ML\models\NaiveBayes.pkl')

    async def predict(self, tweet):
        tweet = self._features(tweet)
        result = joblib.load(r'backend\ML\models\NaiveBayes.pkl').classify(tweet)
        return result
    
if __name__ == "__main__": 
    from nltk.corpus import twitter_samples
    from nltk import download

    # download(['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet', 'averaged_perceptron_tagger'])
    pos_tweet = twitter_samples.strings('positive_tweets.json')
    neg_tweet = twitter_samples.strings('negative_tweets.json')

    model = NaiveBayes(pos_tweet, neg_tweet)
    model._trainmodel()
    