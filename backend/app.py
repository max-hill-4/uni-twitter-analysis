from flask import Flask, request, render_template
from tweet_analysis import analysis_tweets as ta

app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():

    query = request.args.get('query')
    data = ta.get_last_tweet(query)    
    return render_template('search.html', query=data)

if __name__ == '__main__':
    app.run(debug=True)
