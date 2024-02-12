from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('usersdb.sqlite', check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")
db.commit()

def register_user(username, password):
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        return True
    else:
        return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if register_user(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Пользователь с таким именем уже существует.')

    return render_template('register.html')
# Роут для авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            return f'Добро пожаловать, {username}!'
        else:
            return render_template('login.html', error='Неверное имя пользователя или пароль.')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)