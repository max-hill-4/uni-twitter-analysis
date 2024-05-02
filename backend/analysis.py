import get_tweets

class Model:
    def __init__(self, pos_data, neg_data) -> None:
        self.pos_data = pos_data
        self.neg_data = neg_data
    def _preprocess(self):
        pass
    def trainmodel(self):
        pass
    def classify(self):
        pass


async def analyze_tweet(query):
    
    tweet = await get_tweets.get_tweet(query)
    
    NB = None
    NN = None
    data = (tweet, NB, NN)
    return {data}
