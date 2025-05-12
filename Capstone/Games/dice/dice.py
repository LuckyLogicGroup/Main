import random, os, csv

def dice_roll(bet_amount, current_balance, guess, username):
    """Roll a die (1–6), check high/low guess, return outcome and update balance."""
    roll = random.randint(1, 6)
    result = 'High' if roll >= 4 else 'Low'
    win = guess == result

    payout = bet_amount * 2 if win else 0
    net_gain = payout - bet_amount
    new_balance = current_balance + net_gain

    save_dice_history(bet_amount, roll, guess, win, net_gain, new_balance, username)
    return win, roll, result, payout, new_balance

def save_dice_history(bet_amount, roll, guess, win, net_gain, new_balance, username):
    path     = os.path.join(os.path.dirname(__file__), 'dice_results.csv')
    new_file = not os.path.exists(path)

    with open(path, 'a', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['Username', 'Guess', 'Dice Roll', 'Result', 'Bet Amount', 'Net Gain', 'Balance After'])
        w.writerow([
            username, guess, roll,
            'Win' if win else 'Loss',
            bet_amount, net_gain, new_balance
        ])
