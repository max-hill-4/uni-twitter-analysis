import analysis
from flask import Flask, request, render_template

from asyncio import new_event_loop

app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        action = request.args.get('action')  # Get the selected action
        print (action)

        loop = new_event_loop()

        if action == 'user_timeline':
            data = loop.run_until_complete(analysis.analyze_timeline(query))
            return render_template('search.html', twitter_widget=data, sentiment_value= 55)
            
        elif action == 'individual_tweet':
            data = loop.run_until_complete(analysis.analyze_tweet(query))
            return render_template('search.html', twitter_widget=data['html_content'], sentiment_value=data['sentiment_value'])
        else:
            raise ValueError("Invalid action")

        if data is None:
            raise KeyError("Query not found")


    except (KeyError, ValueError):
        error_message = "Not a valid action or tweet. Please try again."
        return render_template('index.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
