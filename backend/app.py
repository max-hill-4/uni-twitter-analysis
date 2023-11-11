from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    # Get the query from the url

    # Give data to the search.html template 
    testdata = request.args.get('query')
    return render_template('search.html', testdata=testdata)

if __name__ == '__main__':
    app.run(debug=True)