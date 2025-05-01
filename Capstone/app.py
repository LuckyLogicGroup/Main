from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess

app = Flask(__name__)
app.secret_key = "slys123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable = False)
    role = db.Column(db.String(10), nullable=False)

#-------------------
#Routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/<role>', methods=['GET'])
def login(role):
    role = role.capitalize()
    return render_template('login.html', role=role)


@app.route("/auth/<role>", methods= ["POST", "PUT"])
def auth(role):
    role = role.capitalize()


    if request.method in ["POST", "PUT"]:
        username = request.form["username"]
        password = request.form["password"]


        user = User.query.filter_by(username=username, role=role).first()
        if user and user.password == password:
            session["username"] = user.username
            session["role"] = role
            return redirect(url_for("homepage"))
        else:
            return "Invalid credentials. Please go back and try again."
    else:
        return "invalid request method"
    
#After login
@app.route('/homepage', methods=["GET"])
def homepage():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('homepage.html', username=session['username'], role=session['role'])

#Games page
@app.route('/games', methods=['GET'])
def games():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('games.html')

@app.route('/games/play')
def play_game():
    game_path = os.path.join('games', 'card_game', 'main.py')

    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'cmd', '/c', 'python', game_path], shell=True)
        else:
            subprocess.Popen(['x-terminal-emulator', '-e', f'python3 {game_path}'], shell=True)

        return redirect(url_for('homepage'))

    except Exception as e:
        return f"Failed to start game: {e}"






@app.route('/games/results')
def download_results():
    csv_path = os.path.join('games', 'card_game', 'probability_challenge_results.csv')
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    else:
        return "Results file not found."
    

#Financial checker page
@app.route('/financial', methods=["GET"])
def financial():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('financial.html')


#history checker page
@app.route('/history', methods=["GET"])
def history():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('history.html')

#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Db setup

def create_user():
    """crate default users."""
    db.create_all()
    defualt_users = [
        {"username": "alex1", "password": "alex234", "role": "User"},
        {"username": "basicuser", "password": "pass212", "role": "User"},
        {"username": "theadmin", "password": "admin2345", "role": "Admin"},
        {"username": "basicadmin", "password": "adminpass", "role": "Admin"},
    ]
    for user_data in defualt_users:
        if not User.query.filter_by(username=user_data["username"]).first():
            user = User(
                username= user_data["username"],
                password=generate_password_hash(user_data["password"]),
                role=user_data["role"]
            )
            db.session.add(user)
        db.session.commit()
        print('Default users created')


@app.cli.command('initdb')
def initdb_command():
    """Intitialling database"""
    create_user



#MAIN
if __name__ == "__main__":
    if not os.path.exists('instance'):
        os.makedirs('instance')
    with app.app_context():
        db.create_all()
    app.run(debug=True)