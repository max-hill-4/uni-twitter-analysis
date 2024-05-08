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
        """"
        Builds Vectoriser and stopwords object to be used in  _preprocess.
        """
        super().__init__()
        # TD: should try to make stopwords static, and data needed for objects static also.
        self._sia = SentimentIntensityAnalyzer()
        self._lemmatizer = WordNetLemmatizer()

        self._tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        
        self._TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }

        self._STOPWORDS = set(stopwords.words("english"))
            
    def _preprocess(self, tweet):
        """
        Cleans data before sentiment analysis, including removing stopwords and alphas.
        Args:
            tweet(str): tweet data of string
        Returns:
            data (list(str)): data that is vectorised and cleaned
        """
        data = self._tokenizer.tokenize(tweet)

        data = [token for token in data if token.isalpha() and token not in self._STOPWORDS]

        # (low) TD: Pull request pos tag (tagset) to work with lemmatize
        data = pos_tag(data)
    
        # (low) TD: refact if data + lemmatize + pos_tag
        
        data = [self._lemmatizer.lemmatize(token, self._TAGMAP.get(pos, 'n')) for token, pos in data]
        
        return data
    
    def _features(self, tweet):
        """
        Calcs the VADER score (from lexicon data)
        Args:
            tweet(str): tweet data of string
        Returns:
            features(dict): dictionary of pos and comp score as keys, to 0-1 float.
        """
        data = self._preprocess(tweet)
        
        if not data:
            return {}

        features = {}
        positive_scores = []
        compound_scores = []

        for word in data:
            positive_scores.append(self._sia.polarity_scores(word)["pos"])
            compound_scores.append(self._sia.polarity_scores(word)["compound"])
        features['pos_score'] = mean(positive_scores)
        features['comp_score'] = mean(compound_scores)
        return features
    
    def _trainmodel(self, ratio: int = 0.15 ):
        """
        Using NLP's NaiveBayes probablity classifier, use labeled data to build 
        a pkl file.
        """
        features = []
        for tweet in self.pos_data:
            features.append((self._features(tweet), 'p'))

        for tweet in self.neg_data:
            features.append((self._features(tweet), 'n'))

        shuffle(features)
        index = int(ratio * len(features))
        classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:index])
        joblib.dump(classifier, r'backend\ML\models\NaiveBayes.pkl')

        return classify.accuracy(classifier, features[index:])

    async def predict(self, tweet):
        """
        By using the trained pkl file in models, classify a single tweet
        Args:
            tweet (str) : text data inside of tweet.
        Returns:
            'p' to indicate positive and 'n' to indicate negative
        """
        print(tweet)
        tweet = self._features(tweet)
        result = joblib.load(r'backend\ML\models\NaiveBayes.pkl').classify(tweet)
        return result

