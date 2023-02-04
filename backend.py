from flask import Flask, request, render_template, flash, redirect

app = Flask(__name__)
app.secret_key = 'p[singasFAfasjmgmd]'

@app.route('/')
def start():
    return render_template('about.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

@app.route('/predictions/send', methods=['POST'])
def get_file():
    print('posted')
    file = request.files
    print(file)
    return ''

app.run(debug=True)