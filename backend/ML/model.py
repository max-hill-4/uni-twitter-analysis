from nltk.corpus import twitter_samples

# Nah but if i get this to work im the goat dude.
class Model:
    def __init__(self):
        self.pos_data = twitter_samples.strings('positive_tweets.json')
        self.neg_data = twitter_samples.strings('negative_tweets.json')
    def _preprocess(self):
        pass
    def _trainmodel(self):
        # data should be here, not in constructor.
        pass
    def _features(self):
        pass
    def _save(self):
        pass
    def predict(self):
        pass