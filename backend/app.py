from flask import Flask, request, render_template, jsonify
from asyncio import new_event_loop
from get_tweets import get_tweet
app = Flask(__name__, template_folder='../frontend/templates')
from ML import NaiveBayes, NeuralNetwork

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    search_query = request.args.get('query')
    return render_template('search.html', q=search_query)

# it might be possible to not need async? as js does the await? maybe im drunk tho.
@app.route('/naivebayes', methods=['GET'])
def naivebayes(data:str):
    loop = new_event_loop()
    data = loop.run_until_complete(NaiveBayes.NaiveBayes().predict(data))
    return data

@app.route('/neuralnetwork/', methods=['GET'])
def neuralnetwork():
    data = request.args.get('data')
    loop = new_event_loop()
    data = loop.run_until_complete(NeuralNetwork.NeuralNetwork().predict(data))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


