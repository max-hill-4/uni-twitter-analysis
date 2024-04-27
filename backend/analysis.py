import get_tweets
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import corpus
from nltk import TweetTokenizer
# If not downloaded: 
from nltk import download
download('vader_lexicon')
download('twitter_samples')
download('stopwords')

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
def train_model():

    words = corpus.twitter_samples.strings()
    stopwords = corpus.stopwords.words("english")
    # remove alphas 

    tokenizer = TweetTokenizer(
    preserve_case=False,
    strip_handles=True,
    reduce_len=True)

    tokens = tokenizer.tokenize(words)

    # possible to do it quicker in pandas!
    for word in words:
        if word in stopwords:
            words.remove(word)
        if word.isalpha():
            words.remove(word)

    print(words[:20])


train_model()



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
