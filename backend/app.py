from flask import Flask, request, render_template
from asyncio import new_event_loop
from get_tweets import get_tweet
app = Flask(__name__, template_folder='../frontend/templates')
from ML import NaiveBayes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(get_tweet(query))
    return render_template('search.html', query=data)

@app.route('/data', methods=['GET'])
def test():
    data = 'test'
    loop = new_event_loop()
    data = loop.run_until_complete(NaiveBayes.NaiveBayes().predict(data))
    return data

if __name__ == '__main__':
    app.run(debug=True, port=5000)


