import Model

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
 
    def _preprocess(self, text):

        lemmatizer = WordNetLemmatizer()


        tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        
        TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }

        STOPWORDS = set(stopwords.words("english"))
        
        tokens = []

        for tweet in self.text:
            
            data = tokenizer.tokenize(tweet)

            data = [token for token in data if token.isalpha() and token not in STOPWORDS]

            # (low) TD: Pull request pos tag (tagset) to work with lemmatize
            data = pos_tag(data)
        
            # (low) TD: refact if data + lemmatize + pos_tag
            
            data = [lemmatizer.lemmatize(token, TAGMAP.get([pos], 'n')) for token, pos in data]
            
            if data:
                self.tokens.append(data)
        return tokens
    
    def trainmodel(self, pos_train, neg_train):
        """
        [({'value' : 1}, 'p'), ]
        """

        # TD : get pre process to return a tuple.
        pos_train = self._preprocess(pos_train)
        neg_train = self._preprocess(neg_train)
        
        # TD: not that happy with label
        label = 'p'
        
        features = []
        sia = SentimentIntensityAnalyzer()
        for categ in pos_train, neg_train:
            for tweet in categ:
                compound_scores = []
                positive_scores = []
                for token in tweet:
                    compound_scores.append(sia.polarity_scores(token)["compound"])
                    positive_scores.append(sia.polarity_scores(token)["pos"])
                features.append(({['comp']: mean(compound_scores),
                                ['pos']: mean(positive_scores)}, label))
            label = 'n'

        shuffle(features)
        classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:1500])
        classifier.show_most_informative_features(5)
        print(classify.accuracy(classifier, features[1500:]))
        return classifier