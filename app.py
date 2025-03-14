from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = "user"
app.secret_key = 'secret_key'


def connect_database(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print("Database connected successfully")
        return connection
    except Error as e:
        print(f"An error occurred: {e}")
        return None


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/sel', methods=['POST', 'GET'])
def render_selection_page():  # put application's code here
    if request.method == 'POST':
        first_name = request.form.get("first_name").title().strip()
        last_name = request.form.get("last_name").title().strip()
        email = request.form.get("email").lower().strip()
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2:
            return redirect("/sel?error=passwords+dont+match")

        if len(password) < 8:
            return redirect("/sel?error=passwords+is+too+short")

        con = connect_database(DATABASE)
        query_insert = "INSERT INTO user (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query_insert, (first_name, last_name, email, password))
        con.commit()
        con.close()

        return redirect("/book")

    return render_template("sel.html")


@app.route('/log', methods=['POST', 'GET'])
def render_login_page():  # put application's code here
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        query = "SELECT user_id, first_name, password FROM user WHERE email = ?"
        con = connect_database(DATABASE)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_info = cur.fetchone()
        con.close()
        print(user_info)

        session['user_id'] = user_info[0]
        session['email'] = user_info[1]

        if email == email and password == password:


    return render_template("log.html")


@app.route('/book')
def render_book_page():  # put application's code here
    return render_template("book.html")


if __name__ == '__main__':
    app.run()
