from cs50 import SQL
from flask import Flask, render_template, redirect, request


app = Flask(__name__, template_folder='templates', static_folder='static')

db =  SQL("postgresql://postgres@localhost/test")


SPORTS = [
    "Basketball",
    "Football",
    "Volleyball"
]


@app.route('/')
def home():
    return render_template('index.html', sports=SPORTS)


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    sport = request.form.get('sport')
    if not name or sport not in SPORTS:
        return render_template('error.html')

    db.execute('INSERT INTO registrants (name, sport) VALUES (?, ?)', name, sport)
    return render_template('register.html')


@app.route('/registrants')
def regs():
    registrants = db.execute('SELECT * FROM registrants')
    return render_template('registrants.html', registrants=registrants)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logged', methods=['POST'])
def log():
    data = db.execute('SELECT * FROM logins')
    username = request.form.get('username')
    password = request.form.get('password')
    found = False

    for u in data:
        if u["username"] == username and u['password'] == password:
            found = True
            break
    if found:
        return render_template('logged.html', username=username)
    else:
        return render_template('error.html')




if __name__ == '__main__':
    app.run(debug=True)
