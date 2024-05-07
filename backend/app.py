from flask import Flask, request, render_template, jsonify
from asyncio import new_event_loop
from get_tweets import get_tweet
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
from ML import NaiveBayes, NeuralNetwork

@app.route('/')
def index():
    """
    Flask route to return the main search page.
    """
    return render_template('index.html')

@app.route('/search')
def search():
    """
    Search page that visualizes the sentiment data of the tweet.
    """
    q = request.args.get('query')
    loop = new_event_loop()
    tweet = loop.run_until_complete(get_tweet(q))
    return render_template('search.html', tweet=tweet)

@app.route('/naivebayes', methods=['GET'])
def naivebayes():
    """
    Uses the ML NaiveBayes Module to perform sentiment analysis.
    Args:
        query (str) : The url of the tweet
    Returns:
        JSON: 'p' or 'n' value dictating sentiment.
    """
    data = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(NaiveBayes.NaiveBayes().predict(data))
    return jsonify(data)

@app.route('/neuralnetwork', methods=['GET'])
def neuralnetwork():
    """
    Uses the ML Neural Netowrk Module to perform sentiment analysis.
    Args:
        query (str) : The url of the tweet
    Returns:
        JSON: 'p' or 'n' value dictating sentiment.
    """
    data = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(NeuralNetwork.NeuralNetwork().predict(data))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


