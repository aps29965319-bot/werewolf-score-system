
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB="dreamwolf.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db=get_db()
    db.execute('''
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        games INTEGER DEFAULT 0,
        mvp INTEGER DEFAULT 0,
        seer_wins INTEGER DEFAULT 0,
        witch_wins INTEGER DEFAULT 0,
        guard_wins INTEGER DEFAULT 0,
        hunter_wins INTEGER DEFAULT 0,
        wolf_wins INTEGER DEFAULT 0,
        villager_wins INTEGER DEFAULT 0
    )
    ''')
    db.commit()
    db.close()

init_db()

@app.route('/')
def home():
    db=get_db()
    players=db.execute('SELECT * FROM players ORDER BY score DESC,wins DESC').fetchall()
    db.close()
    return render_template('index.html',players=players)

@app.route('/add',methods=['POST'])
def add():
    name=request.form.get('name','').strip()
    if name:
        db=get_db()
        db.execute('INSERT INTO players(name) VALUES(?)',(name,))
        db.commit()
        db.close()
    return redirect('/')

def add_stat(pid,col):
    db=get_db()
    db.execute(f'UPDATE players SET {col}={col}+1 WHERE id=?',(pid,))
    db.commit()
    db.close()

@app.route('/win/<int:pid>')
def win(pid):
    db=get_db()
    db.execute('UPDATE players SET score=score+3,wins=wins+1,games=games+1 WHERE id=?',(pid,))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/lose/<int:pid>')
def lose(pid):
    db=get_db()
    db.execute('UPDATE players SET games=games+1 WHERE id=?',(pid,))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/mvp/<int:pid>')
def mvp(pid): add_stat(pid,'mvp'); return redirect('/')
@app.route('/seer/<int:pid>')
def seer(pid): add_stat(pid,'seer_wins'); return redirect('/')
@app.route('/witch/<int:pid>')
def witch(pid): add_stat(pid,'witch_wins'); return redirect('/')
@app.route('/guard/<int:pid>')
def guard(pid): add_stat(pid,'guard_wins'); return redirect('/')
@app.route('/hunter/<int:pid>')
def hunter(pid): add_stat(pid,'hunter_wins'); return redirect('/')
@app.route('/wolf/<int:pid>')
def wolf(pid): add_stat(pid,'wolf_wins'); return redirect('/')
@app.route('/villager/<int:pid>')
def villager(pid): add_stat(pid,'villager_wins'); return redirect('/')

@app.route('/reset/<int:pid>')
def reset(pid):
    db=get_db()
    db.execute('''UPDATE players SET score=0,wins=0,games=0,mvp=0,
    seer_wins=0,witch_wins=0,guard_wins=0,hunter_wins=0,wolf_wins=0,villager_wins=0
    WHERE id=?''',(pid,))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/delete/<int:pid>')
def delete(pid):
    db=get_db()
    db.execute('DELETE FROM players WHERE id=?',(pid,))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/reset_all')
def reset_all():
    db=get_db()
    db.execute('''UPDATE players SET score=0,wins=0,games=0,mvp=0,
    seer_wins=0,witch_wins=0,guard_wins=0,hunter_wins=0,wolf_wins=0,villager_wins=0''')
    db.commit()
    db.close()
    return redirect('/')

if __name__ == '__main__':
    app.run()
