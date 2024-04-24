from flask import Flask, request, render_template
from analysis import analyze_tweet
from asyncio import new_event_loop

app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    loop = new_event_loop()
    data = loop.run_until_complete(analyze_tweet(query))
    return render_template('search.html', query=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
