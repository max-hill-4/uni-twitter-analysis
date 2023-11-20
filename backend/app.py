from flask import Flask, request, render_template
from tweet_analysis import get_tweets as at
import asyncio
app = Flask(__name__, template_folder='../frontend/templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():

    query = request.args.get('query')
    loop = asyncio.new_event_loop()
    data = loop.run_until_complete(at.get_tweet(query))
    return render_template('search.html', query=data)

if __name__ == '__main__':
    app.run(debug=True, port=5555)
