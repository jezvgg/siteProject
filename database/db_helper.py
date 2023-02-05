import sqlite3

class DB_helper:
    con = None
    cur = None

    def __init__(self, path):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.con.cursor()

    def get_table(self, table_name):
        self.cur.execute('SELECT * FROM '+table_name+';')
        result = self.cur.fetchall()
        self.con.commit()
        return result

    def get_pred(self):
        column_teams = []
        column_scores = []
        for row in self.get_table('predictions'):
            column_teams.append(row[0])
            column_scores.append(row[1])
        return {'team':column_teams,'score':column_scores}

    def exucation(self, prop):
        self.cur.execute(prop)
        self.con.commit()
        return 'All done'

    def ex_predictions(self, team, pred):
        ex = 'INSERT INTO predictions(Team, Score) VALUES("'+team+'",'+str(pred)+');'
        print(ex)
        return self.exucation(ex)