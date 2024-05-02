from analysis import Model

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
 
    def _preprocess(self, tweet):

        lemmatizer = WordNetLemmatizer()


        tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        
        TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }

        STOPWORDS = set(stopwords.words("english"))
        
        data = tokenizer.tokenize(tweet)

        data = [token for token in data if token.isalpha() and token not in STOPWORDS]

        # (low) TD: Pull request pos tag (tagset) to work with lemmatize
        data = pos_tag(data)
    
        # (low) TD: refact if data + lemmatize + pos_tag
        
        data = [lemmatizer.lemmatize(token, TAGMAP.get(pos, 'n')) for token, pos in data]
        
        return data
    
    def _features(self, tweet):

        data = self._preprocess(tweet)
        if not data:
            return {}
        sia = SentimentIntensityAnalyzer()
        features = {}
        positive_scores = []
        compound_scores = []

        for word in data:
            positive_scores.append(sia.polarity_scores(word)["pos"])
            compound_scores.append(sia.polarity_scores(word)["compound"])
        features['pos_score'] = mean(positive_scores)
        features['comp_score'] = mean(compound_scores)
        return features
    
    def trainmodel(self):
        # honestly it feels really slow 
        # i suspect its becuase its doing somany method calls? 
        # im guessing i also iterate over the data 1 million times tbh!
        features = []

        for tweet in self.pos_data:
            features.append((self._features(tweet), 'p'))

        for tweet in self.neg_data:
            features.append((self._features(tweet), 'n'))

        shuffle(features)
        classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:1500])
        classifier.show_most_informative_features(5)
        print(classify.accuracy(classifier, features[1500:]))
        return True
    
    def classify(self):
        pass
if __name__ == "__main__": 
    from nltk.corpus import twitter_samples
    from nltk import download

    download(['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet', 'averaged_perceptron_tagger'])
    pos_tweet = twitter_samples.strings('positive_tweets.json')
    neg_tweet = twitter_samples.strings('negative_tweets.json')

    model = NaiveBayes(pos_tweet, neg_tweet)
    trained = model.trainmodel()