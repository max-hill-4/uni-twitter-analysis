from model import Model

from nltk import pos_tag
from nltk import NaiveBayesClassifier
from nltk import classify
from nltk import TweetTokenizer

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from random import shuffle
from statistics import mean


class NaiveBayes(Model):
    def __init__(self, pos_data, neg_data) -> None:
        self.pos_data = pos_data
        self.neg_data = neg_data
        
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
    
    def features(self, tweet):

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
    
    def trainmodel(self):

        features = []

        for tweet in self.pos_data:
            features.append((self.features(tweet), 'p'))

        for tweet in self.neg_data:
            features.append((self.features(tweet), 'n'))

        shuffle(features)
        self.classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:1500])
        self.classifier.show_most_informative_features(5)
        self.accuracy = classify.accuracy(self.classifier, features[1500:])
    
    def score(self, tweet):
        result = self.classifier.classify(tweet)
        return (f'I am {self.accuracy*100} sure it is {result} ')

if __name__ == "__main__": 
    from nltk.corpus import twitter_samples
    from nltk import download

    download(['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet', 'averaged_perceptron_tagger'])
    pos_tweet = twitter_samples.strings('positive_tweets.json')
    neg_tweet = twitter_samples.strings('negative_tweets.json')

    model = NaiveBayes(pos_tweet, neg_tweet)
    # I HATE THIS SO MUCH PLEASE TD: HIGH HIGH HIGH!
    model.trainmodel()
    
    test_data = model.features("Hi i am good good test positive happy")
    
    print(model.score(test_data))