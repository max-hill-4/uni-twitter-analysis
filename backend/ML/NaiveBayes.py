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
<<<<<<< Updated upstream

        data = self.tokenizer.tokenize(tweet)

        data = [token for token in data if token.isalpha() and token not in self.STOPWORDS]

=======
        """
        Cleans data before sentiment analysis, including removing stopwords and alphas.
        Args:
            tweet(str): tweet data of string
        Returns:
            data (list(str)): data that is vectorised and cleaned
        """
        testing_output = []
        testing_output.append(tweet)
        data = self._tokenizer.tokenize(tweet)
        testing_output.append(data)

        data = [token for token in data if token.isalpha() and token not in self._STOPWORDS]
        testing_output.append(data)
>>>>>>> Stashed changes
        # (low) TD: Pull request pos tag (tagset) to work with lemmatize
        data = pos_tag(data)

        # (low) TD: refact if data + lemmatize + pos_tag
        
<<<<<<< Updated upstream
        data = [self.lemmatizer.lemmatize(token, self.TAGMAP.get(pos, 'n')) for token, pos in data]
        
=======
        data = [self._lemmatizer.lemmatize(token, self._TAGMAP.get(pos, 'n')) for token, pos in data]
        testing_output.append(data)
        print(testing_output)
>>>>>>> Stashed changes
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
        print(tweet)
        tweet = self._features(tweet)
        result = joblib.load(r'backend\ML\models\NaiveBayes.pkl').classify(tweet)
        return result
    
if __name__ == "__main__": 
    from nltk import download
    download(['wordnet'])
