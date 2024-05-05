from flask import Flask, request, render_template, jsonify
from asyncio import new_event_loop
from get_tweets import get_tweet
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
from ML import NaiveBayes, NeuralNetwork

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/naivebayes', methods=['GET'])
def naivebayes():
    data = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(NaiveBayes.NaiveBayes().predict(data))
    return jsonify(data)

@app.route('/neuralnetwork', methods=['GET'])
def neuralnetwork():
    data = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(NeuralNetwork.NeuralNetwork().predict(data))
    return jsonify(data)

@app.route('/twitterembed')
def twitterembed():
    data = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(get_tweet(data))
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)


