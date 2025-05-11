import random, os, csv

# ------------------  COINFLIP  ------------------
def coinflip_spin(bet_amount, current_balance, username):
    """Return win?, result, payout, new_balance and log the flip."""
    outcome = random.choice(['Heads', 'Tails'])
    win = random.choice([True, False]) 

    payout = bet_amount * 2 if win else 0
    net_gain = payout - bet_amount
    new_balance = current_balance + net_gain

    save_coinflip_history(bet_amount, outcome, win, net_gain, new_balance, username)
    return win, outcome, payout, new_balance

# ---------------  CSV LOGGING  -----------------
def save_coinflip_history(bet_amount, outcome, win, net_gain, new_balance, username):
    path     = os.path.join(os.path.dirname(__file__), 'coinflip_results.csv')
    new_file = not os.path.exists(path)

    with open(path, 'a', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['Username','Outcome','Bet Amount','Result','Net Gain','Balance After'])
        w.writerow([
            username, outcome, bet_amount,
            'Win' if win else 'Loss', net_gain, new_balance
        ])
