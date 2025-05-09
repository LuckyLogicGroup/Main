import random, os, csv

# --------------------  SPIN  --------------------
def spin_roulette(bet_type, bet_value, bet_amount, current_balance, username):
    """Return win?, landed_number, landed_color, payout, new_balance
       and log the spin with username."""
    numbers = list(range(37))
    landed_number = random.choice(numbers)
    landed_color  = 'Green' if landed_number==0 else random.choice(['Red','Black'])

    win, payout = False, 0
    if bet_type=='color'  and bet_value.capitalize()==landed_color:
        win, payout = True, bet_amount*2
    elif bet_type=='number' and int(bet_value)==landed_number:
        win, payout = True, bet_amount*36

    net_gain    = payout - bet_amount if win else -bet_amount
    new_balance = current_balance + net_gain

    save_to_history(bet_type, bet_value, bet_amount,
                    win, net_gain, new_balance, username)
    return win, landed_number, landed_color, payout, new_balance

# ------------------  CSV LOG  -------------------
def save_to_history(bet_type, bet_value, bet_amount,
                    win, net_gain, new_balance, username):
    path     = os.path.join(os.path.dirname(__file__), 'roulette_results.csv')
    new_file = not os.path.exists(path)

    with open(path, 'a', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['Username','Bet Type','Bet Value','Bet Amount',
                        'Result','Net Gain','Balance After'])
        w.writerow([
            username, bet_type, bet_value, bet_amount,
            'Win' if win else 'Loss', net_gain, new_balance
        ])
