import get_tweets

from string import punctuation
from random import shuffle

from nltk import pos_tag
from nltk import TweetTokenizer
from nltk import download
from nltk import NaiveBayesClassifier
from nltk import classify
from nltk import FreqDist

from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples

from statistics import mean

corpora = ['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
# (low) check if corpara exists.
for i in corpora:
     download(i)

"""
TD? 

-> use pandas for data - its getting confusing!

-> are we going to train a entire model using a classifier everytime I load the program? 
-> could i create train model and use an api to call to it? 

->  i iterate twice (data pp + model train)

-> return important features (highlight?)

-> plot visual data DL


References: 
real python
https://necromuralist.github.io/Neurotic-Networking/posts/nlp/01-twitter-preprocessing-with-nltk/index.html
"""
class ProcessData:
    def __init__(self, text: list):
        self.text = text
        self.STOPWORDS = set(stopwords.words("english"))
        
        self.tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        
        self.lemmatizer = WordNetLemmatizer()

        self.TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }


    def map_pos(self,tag: list):
                
        return self.TAGMAP.get(tag[0], 'n')
        

    def process_text(self) -> list[list[str]]:
        
        tokens = []

        for tweet in self.text:
            
            data = self.tokenizer.tokenize(tweet)

            data = [token for token in data if token.isalpha() and token not in self.STOPWORDS]

            # (low) TD: Pull request pos tag (tagset) to work with lemmatize
            data = pos_tag(data)
        
            # (low) TD: refact if data + lemmatize + pos_tag
            
            data = [self.lemmatizer.lemmatize(token, self.map_pos(pos)) for token, pos in data]
            
            if data:
                tokens.append(data)
        
        return tokens
    
class TrainModel:

    def __init__(self, pos_text, neg_text):
        
        self.sia = SentimentIntensityAnalyzer()
        self._pos_text = pos_text
        self._neg_text = neg_text

        self._freq = FreqDist([item for sublist in pos_text for item in sublist])
        
        self._bow = [word for word, _ in self._freq.most_common(10)]
    
    def _calc_tweet(self, tweet) -> dict:
        features = {}
        compound_scores = []
        positive_scores = []
        bow = 0
        for word in tweet:
            compound_scores.append(self.sia.polarity_scores(word)["compound"])
            positive_scores.append(self.sia.polarity_scores(word)["pos"])
            if word in self._bow:  
                bow += 1
        
        features['mean_compound'] = mean(compound_scores) 
        features['mean_positive'] = mean(positive_scores)
        # it actually became less accurate with this data lol!
        features['bow'] = bow

        return features


    def train(self):
     
        # [({'value' : 1}, 'p'), ]
        features = []
        for tweet in self._pos_text:
            features.append((self._calc_tweet(tweet), 'p'))
        
        for tweet in self._neg_text:
            features.append((self._calc_tweet(tweet), 'n'))
         
        shuffle(features)
        classifier = NaiveBayesClassifier.train(labeled_featuresets=features[:1500])
        classifier.show_most_informative_features(5)
        print(classify.accuracy(classifier, features[1500:]))
        return classifier
    
# should have a function in proccess data so i can just read(*.txt)

pos_tweet = twitter_samples.strings('positive_tweets.json')
neg_tweet = twitter_samples.strings('negative_tweets.json')

pos_data = ProcessData(pos_tweet).process_text()
neg_data = ProcessData(neg_tweet).process_text()


model = TrainModel(pos_data, neg_data).train()


# im going to seperate the texts, it helps with empty labels + freqdist.







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
