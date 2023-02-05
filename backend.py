from flask import Flask, request, render_template, send_from_directory, redirect
from sklearn.metrics import accuracy_score
from database.db_helper import DB_helper
import pandas as pd

data_true = pd.read_csv('dataset/public.csv')
help = DB_helper('database/predictions.db')

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

@app.route('/predictions', methods=['POST', 'GET'])
def predictions():
    result='Файл ещё не загружен.'
    
    if request.method == 'POST':
        file = request.files['file']

        try:
            df = pd.read_csv(file)
            acc = accuracy_score(df['label'], data_true['label'])
            result = 'Результат: '+str(acc)
            print(help.ex_predictions(request.values['team'], acc))
        except UnicodeDecodeError:
            print('Cant read file')
            result = 'Неполучается считать файл.'
        except KeyError:
            print('Not this csv')
            result='Неверный формат csv файла.'
        return {'result':result}

    return render_template('predictions.html', result=result)

@app.route('/data/get')
def get_data():
    print(app.static_folder)
    redirect('http://127.0.0.1:5000/data')
    return send_from_directory(app.static_folder, 'data.zip', mimetype = 'zip')

@app.route('/leaderboard')
def view_leaderboard():
    preds = help.get_pred()
    result = {}

    for row in range(len(preds['team'])):
        if preds['team'][row] not in result.keys():
            result[preds['team'][row]] = preds['score'][row]

        elif result[preds['team'][row]]<preds['score'][row]:
            result[preds['team'][row]] = preds['score'][row]

    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

    return render_template('leaderboard.html', data=result)

app.run(debug=True)