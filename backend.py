from flask import Flask, request, render_template, send_from_directory, redirect
from sklearn.metrics import accuracy_score
from database.db_helper import DB_helper
import pandas as pd
import os

# Загружаем CSV файл для анализа
current_path = os.path.split(__file__)
public_file = "%s/dataset/public.csv" % (current_path[0])
if not os.path.exists(public_file):
        raise Exception("ERROR: Невозможно запустить сайт. Не найден файл с данными  %s", public_file)

data_true = pd.read_csv(public_file)

# Подключаем базу данных
database_file = "%s/database/predictions.db" % (current_path[0])
if not os.path.exists(database_file):
        raise Exception("ERROR: Невозможно запустить сайт. Не найден файл базы данных  %s", database_file)

help = DB_helper(database_file)


# Запуск Rest Api
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

@app.route('/data/base')
def get_base():
    print(app.static_folder)
    redirect('http://127.0.0.1:5000/data')
    return send_from_directory(app.static_folder, 'baseline.zip', mimetype = 'zip')

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