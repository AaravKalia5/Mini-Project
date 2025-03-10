from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

@app.route('/sel')
def render_selection_page():  # put application's code here
    return render_template("sel.html")


if __name__ == '__main__':
    app.run()
