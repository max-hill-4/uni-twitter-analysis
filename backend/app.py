from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)