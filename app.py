from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

@app.route('/sel', methods=['POST', 'GET'])
def render_selection_page():  # put application's code here
    if request.method == 'POST':
        fname = request.form.get("user_fname").title().strip()
        lname = request.form.get("user_lname").title().strip()
        email = request.form.get("email").lower().strip()
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2:
            return redirect("/sel?error=passwords+dont+match")


        if len(password) < 8:
            return redirect("/sel?error=passwords+is+too+short")

    return render_template("sel.html")


@app.route('/log', methods=['POST', 'GET'])
def render_login_page():  # put application's code here
    return render_template("log.html")

if __name__ == '__main__':
    app.run()
