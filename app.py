from flask import Flask, render_template
app=Flask(__name__)
players=[{'name':'玩家A','score':30},{'name':'玩家B','score':25}]
@app.route('/')
def home():
    return render_template('index.html',players=players)
if __name__=='__main__':
    app.run()
