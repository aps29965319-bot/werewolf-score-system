
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
    mvp INTEGER DEFAULT 0)""")
    conn.commit()
    conn.close()
init()

@app.route("/")
def home():
    conn=db()
    players=conn.execute("SELECT * FROM players ORDER BY score DESC").fetchall()
    conn.close()
    return render_template("index.html",players=players)

@app.route("/add",methods=["POST"])
def add():
    name=request.form["name"]
    conn=db()
    conn.execute("INSERT INTO players(name) VALUES(?)",(name,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/win/<int:pid>")
def win(pid):
    conn=db()
    conn.execute("UPDATE players SET wins=wins+1,games=games+1,score=score+3 WHERE id=?",(pid,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/lose/<int:pid>")
def lose(pid):
    conn=db()
    conn.execute("UPDATE players SET games=games+1 WHERE id=?",(pid,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/mvp/<int:pid>")
def mvp(pid):
    conn=db()
    conn.execute("UPDATE players SET mvp=mvp+1,score=score+1 WHERE id=?",(pid,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__=="__main__":
    app.run()
