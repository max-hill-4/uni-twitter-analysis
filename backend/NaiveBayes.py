import Model

from nltk import pos_tag
from nltk import NaiveBayesClassifier
from nltk import classify

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from random import shuffle


class NaiveBayes(Model):
    def _preprocess(self):
        """
        return:[({'value' : 1}, 'p'), ]
        """

        self.tokens = []

        for tweet in self.text:
            
            data = self.tokenizer.tokenize(tweet)

            data = [token for token in data if token.isalpha() and token not in self.STOPWORDS]

            # (low) TD: Pull request pos tag (tagset) to work with lemmatize
            data = pos_tag(data)
        
            # (low) TD: refact if data + lemmatize + pos_tag
            
            data = [self.lemmatizer.lemmatize(token, self.map_pos(pos)) for token, pos in data]
            
            if data:
                self.tokens.append(data)
        
    
    def trainmodel(self):
        features = []
        sia = SentimentIntensityAnalyzer()

        for tweet in self.tokens:
            compound_scores = []
            positive_scores = []
            for token in tweet:
                compound_scores.append(sia.polarity_scores(token)["compound"])
                positive_scores.append(sia.polarity_scores(token)["pos"])


        shuffle(features)
        classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:1500])
        classifier.show_most_informative_features(5)
        print(classify.accuracy(classifier, features[1500:]))
        return classifier