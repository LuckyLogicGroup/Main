import os, csv, subprocess
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from Games.roulette.roulette import spin_roulette          # ← lowercase import
from Games.coinflip.coinflip import coinflip_spin
from Games.dice.dice import dice_roll
from Games.slots.slots import slots_spin

app = Flask(__name__)
app.secret_key = "slys123"

# ----------------  DATABASE  -----------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir,'instance','database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(10),  nullable=False)          # User / Admin

# ----------------  AUTH / LOGIN  -------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<role>')
def login(role):
    return render_template('login.html', role=role.capitalize())

@app.route('/auth/<role>', methods=['POST'])
def auth(role):
    u = request.form['username']; p = request.form['password']
    user = User.query.filter_by(username=u, role=role.capitalize()).first()
    if user and check_password_hash(user.password, p):
        session.update(username=user.username, role=user.role, balance=100)
        return redirect(url_for('homepage'))
    return "Invalid credentials", 401

@app.route('/signup')
def signup():
    return render_template('signup.html', role='user')

@app.route('/register/<role>', methods=['POST'])
def register(role):
    u = request.form['username']
    p = request.form['password']
    existing_user = User.query.filter_by(username=u).first()
    if existing_user:
        return "Username already taken", 400
    new_user = User(username=u, password=generate_password_hash(p), role=role.capitalize())
    db.session.add(new_user)
    db.session.commit()
    session.update(username=u, role=role.capitalize(), balance=100)
    return redirect(url_for('homepage'))

# ----------------  PAGES  --------------------
@app.route('/homepage')
def homepage():
    if 'username' not in session: return redirect(url_for('index'))
    return render_template('homepage.html', username=session['username'])

@app.route('/games')
def games():
    if 'username' not in session: return redirect(url_for('index'))
    return render_template('games.html')

@app.route('/games/play')
def play_game():
    path = os.path.join('Games','card_game','main.py')
    if os.name=='nt':
        subprocess.Popen(['start','cmd','/c','python',path], shell=True)
    else:
        subprocess.Popen(['x-terminal-emulator','-e',f'python3 {path}'], shell=True)
    return redirect(url_for('games'))

@app.route('/games/results')
def download_results():
    csv_path = os.path.join('Games','card_game','probability_challenge_results.csv')
    return send_file(csv_path, as_attachment=True) if os.path.exists(csv_path) else "No CSV yet."

# -----------  GIVE EXTRA COINS  --------------
@app.route('/get_more_coins')
def get_more_coins():
    if 'username' not in session: return redirect(url_for('index'))
    session['balance'] += 100
    return redirect(url_for('roulette'))

# ---------------  ROULETTE  ------------------
@app.route('/roulette', methods=['GET','POST'])
def roulette():
    if 'username' not in session: return redirect(url_for('index'))

    if request.method == 'POST':
        bt = request.form['bet_type']
        bv = request.form['bet_value']
        ba = int(request.form['bet_amount'])
        if ba > session['balance']: return "Not enough coins!", 400

        win, num, col, payout, new_bal = spin_roulette(
            bt, bv, ba, session['balance'], session['username']   # pass username!
        )
        session['balance'] = new_bal
        return redirect(url_for('roulette'))

    return render_template('roulette.html', balance=session.get('balance',100))

# ---------------  COINFLIP  ------------------
@app.route('/coinflip', methods=['GET', 'POST'])
def coinflip():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        bet_amount = int(request.form['bet_amount'])
        if bet_amount > session['balance']:
            return "Not enough coins!", 400

        win, outcome, payout, new_balance = coinflip_spin(
            bet_amount, session['balance'], session['username']
        )
        session['balance'] = new_balance
        return redirect(url_for('coinflip'))

    return render_template('coinflip.html', balance=session.get('balance', 100))

# ---------------  DICE  ------------------
@app.route('/dice', methods=['GET', 'POST'])
def dice():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        bet_amount = int(request.form['bet_amount'])
        guess = request.form['guess']
        if bet_amount > session['balance']:
            return "Not enough coins!", 400

        win, roll, result, payout, new_balance = dice_roll(
            bet_amount, session['balance'], guess, session['username']
        )
        session['balance'] = new_balance
        return redirect(url_for('dice'))

    return render_template('dice.html', balance=session.get('balance', 100))

# ---------------  SLOTS  ------------------
@app.route('/slots', methods=['GET', 'POST'])
def slots():
    if 'username' not in session:
        return redirect(url_for('index'))

    slots_result, result = None, None

    if request.method == 'POST':
        bet_amount = int(request.form['bet_amount'])
        if bet_amount > session['balance']:
            return "Not enough coins!", 400

        slots_result, result, win, payout, new_balance = slots_spin(
            bet_amount, session['balance'], session['username']
        )
        session['balance'] = new_balance

    return render_template('slots.html',
        balance=session.get('balance', 100),
        slots=slots_result,
        result=result
    )

# ---------------  HISTORY  -------------------
@app.route('/history')
def history():
    if 'username' not in session: return redirect(url_for('index'))

    # Load Roulette History
    roulette_path = os.path.join('Games', 'roulette', 'roulette_results.csv')
    roulette_rows = []
    if os.path.exists(roulette_path):
        with open(roulette_path) as f:
            rdr = csv.reader(f); next(rdr, None)
            for r in rdr:
                if session['role'] == 'Admin' or r[0] == session['username']:
                    roulette_rows.append(r)

    # Load Coinflip History
    coinflip_path = os.path.join('Games', 'coinflip', 'coinflip_results.csv')
    coinflip_rows = []
    if os.path.exists(coinflip_path):
        with open(coinflip_path) as f:
            rdr = csv.reader(f); next(rdr, None)
            for r in rdr:
                if session['role'] == 'Admin' or r[0] == session['username']:
                    coinflip_rows.append(r)

    # Card Game link (optional)
    card_csv = os.path.join('Games', 'card_game', 'probability_challenge_results.csv')

    # Load Dice History
    dice_path = os.path.join('Games', 'dice', 'dice_results.csv')
    dice_rows = []
    if os.path.exists(dice_path):
        with open(dice_path) as f:
            rdr = csv.reader(f); next(rdr, None)
            for r in rdr:
                if session['role'] == 'Admin' or r[0] == session['username']:
                    dice_rows.append(r)

    # Load Slots History
    slots_path = os.path.join('Games', 'slots', 'slots_results.csv')
    slots_rows = []
    if os.path.exists(slots_path):
        with open(slots_path, 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            next(rdr, None)
            for r in rdr:
                if session['role'] == 'Admin' or r[0] == session['username']:
                    slots_rows.append(r)

    return render_template('history.html',
        roulette_rows=roulette_rows,
        coinflip_rows=coinflip_rows,
        dice_rows=dice_rows,
        slots_rows=slots_rows,
        is_admin=(session['role'] == 'Admin'),
        show_card_link=os.path.exists(card_csv)
    )

# ---------------  LOGOUT ---------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ---------------  INIT DB  -------------------
def create_default_users():
    defaults = [
        ("alex1",     "alex234",   "User"),
        ("basicuser", "pass212",   "User"),
        ("theadmin",  "admin2345", "Admin"),
        ("basicadmin","adminpass", "Admin"),
    ]
    for u,p,r in defaults:
        if not User.query.filter_by(username=u).first():
            db.session.add(User(username=u,
                                password=generate_password_hash(p), role=r))
    db.session.commit()
    
# ---------------  MAIN  ----------------------
if __name__ == "__main__":
    os.makedirs('instance', exist_ok=True)
    with app.app_context(): db.create_all(); create_default_users()
    app.run(debug=True)
