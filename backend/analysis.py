import get_tweets
from string import punctuation

from nltk import pos_tag
from nltk import TweetTokenizer
from nltk import download
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples

from statistics import mean

corpora = ['vader_lexicon', 'twitter_samples', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
# Need to find way to check if already installed
for i in corpora:
     download(i)

"""
Designing my own model: 

-> Tokenize all of the text
-> Remove Stop Words ( I, Me, And )
-> Lemmatization - ( Group words, run running)
-> POS tagging improves Lemmatization alot, Nouns are not Sentiment!
-> Feature Selection
    Tag the data with our 'feature data' - (Frequency, VADER score , etc.)
    Tag the data with the positive or negative 'actual' data

-> Train classification models

-> Compare the classification models

TD? 
-> are we going to train a entire model using a classifier everytime I load the program? 
-> could i create train model and use an api to call to it? 

https://necromuralist.github.io/Neurotic-Networking/posts/nlp/01-twitter-preprocessing-with-nltk/index.html
"""

class ProcessData:

    def __init__(self, text: list):
        # Text is passed as unclean data.
        self.text = text
        self.tokens = []
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))
        self.tokenizer = TweetTokenizer(preserve_case=False,
                                        strip_handles=True,
                                        reduce_len=True)
        self. TAGMAP = {'V' : 'v', 'J' : 'a', 'N' : 'n', 'R' : 'r' }


    def convert_pos(self,tag: list):
                
        # noun if not found as a tag.
        
        return self.TAGMAP.get(tag[0], 'n')
        

    def process_text(self) -> list[list[str]]:
        
        for sentence in self.text:
            data = []
            # tokenize the sentence
            data = self.tokenizer.tokenize(sentence)

            # remove stopwords
            data = [token for token in data if token.isalpha() and token not in self.stopwords]

            # Pull request needed for pos tag -> lemmas tag!
            data = pos_tag(data)
        
            # need to map pos tags to correct lemmatize tags!
            data = [self.lemmatizer.lemmatize(token, self.convert_pos(pos)) for token, pos in data]
            self.tokens.append(data)
        
        return self.tokens
    
class TrainModel:
    """
    Each item in this list of features needs to be a tuple whose first item is the dictionary
    returned by extract_features and whose second item is the predefined category for the text.
    After initially training the classifier with some data that has already been 
    categorized (such as the movie_reviews corpus), you’ll be able to classify new data.
    """
    def __init__(self, text):
        self.text = text
        self.sia = SentimentIntensityAnalyzer()
    
    def extract_features(self, tweet: list[str]) -> dict:

        if not tweet:
            return False

        features = {}
        compound_scores = []
        positive_scores = []

        for word in tweet:
            compound_scores.append(self.sia.polarity_scores(word)["compound"])
            positive_scores.append(self.sia.polarity_scores(word)["pos"])

        # might need to add one to ensure pos scores
        
        features['mean_compound'] = mean(compound_scores) 
        features['mean_positive'] = mean(positive_scores)
        if features['mean_compound'] == 0:
            print(f'{tweet} has a compound of 0!')

        return features

    def create_features_list(self, text: list[list[str]], pos: bool):
        features = []

        for tweet in text:
            features.append((self.extract_features(tweet), pos))
        
        return features
    
tweet = twitter_samples.strings('positive_tweets.json')
data = ProcessData(tweet)
cleaned_text = data.process_text()
model = TrainModel(cleaned_text)

print(model.create_features_list(cleaned_text,1))





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
