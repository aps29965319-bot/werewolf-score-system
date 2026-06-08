
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    conn = sqlite3.connect("werewolf.db")
    conn.row_factory = sqlite3.Row
    return conn

def init():
    conn=db()
    conn.execute("""CREATE TABLE IF NOT EXISTS players(
    id INTEGER PRIMARY KEY,
    name TEXT,
    score INTEGER DEFAULT 0,
    games INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    mvp INTEGER DEFAULT 0,
    seer_win INTEGER DEFAULT 0,
    witch_win INTEGER DEFAULT 0,
    guard_win INTEGER DEFAULT 0,
    hunter_win INTEGER DEFAULT 0,
    wolf_win INTEGER DEFAULT 0,
    villager_win INTEGER DEFAULT 0
    )""")
    conn.commit()
    conn.close()

init()

@app.route("/")
def home():
    conn=db()
    players=conn.execute("SELECT * FROM players ORDER BY score DESC,wins DESC").fetchall()
    conn.close()
    return render_template("index.html",players=players)

@app.route("/add",methods=["POST"])
def add():
    conn=db()
    conn.execute("INSERT INTO players(name) VALUES(?)",(request.form["name"],))
    conn.commit()
    conn.close()
    return redirect("/")

def rolewin(pid,col):
    conn=db()
    conn.execute(f"UPDATE players SET {col}={col}+1 WHERE id=?",(pid,))
    conn.commit()
    conn.close()

@app.route("/win/<int:pid>")
def win(pid):
    conn=db()
    conn.execute("UPDATE players SET wins=wins+1,games=games+1,score=score+3 WHERE id=?",(pid,))
    conn.commit(); conn.close()
    return redirect("/")

@app.route("/lose/<int:pid>")
def lose(pid):
    conn=db()
    conn.execute("UPDATE players SET losses=losses+1,games=games+1 WHERE id=?",(pid,))
    conn.commit(); conn.close()
    return redirect("/")

@app.route("/mvp/<int:pid>")
def mvp(pid):
    conn=db()
    conn.execute("UPDATE players SET mvp=mvp+1,score=score+1 WHERE id=?",(pid,))
    conn.commit(); conn.close()
    return redirect("/")

@app.route("/seer/<int:pid>")
def seer(pid): rolewin(pid,"seer_win"); return redirect("/")

@app.route("/witch/<int:pid>")
def witch(pid): rolewin(pid,"witch_win"); return redirect("/")

@app.route("/guard/<int:pid>")
def guard(pid): rolewin(pid,"guard_win"); return redirect("/")

@app.route("/hunter/<int:pid>")
def hunter(pid): rolewin(pid,"hunter_win"); return redirect("/")

@app.route("/wolf/<int:pid>")
def wolf(pid): rolewin(pid,"wolf_win"); return redirect("/")

@app.route("/villager/<int:pid>")
def villager(pid): rolewin(pid,"villager_win"); return redirect("/")

@app.route("/reset_player/<int:pid>")
def reset_player(pid):
    conn=db()
    conn.execute("""UPDATE players SET score=0,games=0,wins=0,losses=0,mvp=0,
    seer_win=0,witch_win=0,guard_win=0,hunter_win=0,wolf_win=0,villager_win=0
    WHERE id=?""",(pid,))
    conn.commit(); conn.close()
    return redirect("/")
