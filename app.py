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
   con = connect_database(DATABASE)
   cur = con.cursor()
   query = "SELECT user_id, tutor_name, subject, location, time FROM book"
   cur.execute(query)
   book = cur.fetchall()
   con.close()
   return render_template("index.html", book = book)




@app.route('/sel', methods=['POST', 'GET'])
def render_selection_page():  # put application's code here
   if request.method == 'POST':
       first_name = request.form.get("first_name").title().strip()
       last_name = request.form.get("last_name").title().strip()
       email = request.form.get("email").lower().strip()
       password = request.form.get("password")
       password2 = request.form.get("password2")
       role = request.form.get("role")


       if password != password2:
           return redirect("/sel?error=passwords+dont+match")


       if len(password) < 8:
           return redirect("/sel?error=passwords+is+too+short")


       con = connect_database(DATABASE)
       query_insert = "INSERT INTO user (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)"
       cur = con.cursor()
       cur.execute(query_insert, (first_name, last_name, email, password, role))
       con.commit()
       con.close()


       if role == 'Student':
           return redirect('/book')


       else:
           return redirect('/')


   return render_template("sel.html")




@app.route('/log', methods=['POST', 'GET'])
def render_login_page():  # put application's code here
   if request.method == 'POST':
       email = request.form['email'].strip().lower()
       password = request.form['password']


       query = "SELECT user_id, first_name, password, role FROM user WHERE email = ?"
       con = connect_database(DATABASE)
       cur = con.cursor()
       cur.execute(query, (email,))
       user_info = cur.fetchone()
       con.close()
       print(user_info)


       if user_info is None:
           return redirect('/sel')


       stored_password = user_info[2]
       if stored_password != password:
           return redirect("/log?error=incorrect+password")


       session['user_id'] = user_info[0]
       session['email'] = user_info[1]
       session['role'] = user_info[3]


       if user_info[3] == 'Student':
           return redirect('/book')


       else:
           return redirect('/')










   return render_template("log.html")




@app.route('/book', methods=['GET', 'POST'])
def render_book_page():  # put application's code here
   con = connect_database(DATABASE)
   query = "SELECT first_name, last_name FROM user WHERE role = 'Tutor'"
   cur = con.cursor()
   cur.execute(query)
   tutors = cur.fetchall()
   con.close()


   if request.method == 'POST':
       tutor_name = request.form['tutor_name']
       subject = request.form['subject']
       location = request.form['location']
       time = request.form['time']


       con = connect_database(DATABASE)
       query_insert = "INSERT INTO book (user_id, tutor_name, subject, location, time) VALUES (?,?,?,?,?)"
       cur = con.cursor()
       cur.execute(query_insert, (session['user_id'], tutor_name, subject, location, time))
       con.commit()
       con.close()


       return redirect('/')


   return render_template("book.html", tutors=tutors)




@app.route('/req')
def render_request_page():  # put application's code here
   return render_template("req.html")












if __name__ == '__main__':
   app.run()

