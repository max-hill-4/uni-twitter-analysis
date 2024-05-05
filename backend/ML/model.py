from nltk.corpus import twitter_samples
from nltk.data import path
import os

path.append(os.getcwd() + r"\backend\ML\data")

class Model:
    def __init__(self):
        self.pos_data = twitter_samples.strings('positive_tweets.json')
        self.neg_data = twitter_samples.strings('negative_tweets.json')
    def _preprocess(self):
        pass
    def _trainmodel(self):
        pass
    def _features(self):
        pass
    def _save(self):
        pass
    def predict(self):
        pass