import random, os, csv

EMOJIS = ['🍒', '🍋', '🍉', '⭐', '🔔', '💎']

def slots_spin(bet_amount, current_balance, username):
    slots = [random.choice(EMOJIS) for _ in range(3)]

    if slots.count(slots[0]) == 3:
        payout = bet_amount * 5  # Jackpot multiplier
        result = f'Jackpot! x5 Multiplier'
        win = True
    elif len(set(slots)) == 2:
        payout = bet_amount * 2  # Any two matching emojis
        result = f'Double Match x2 Multiplier'
        win = True
    else:
        payout = 0
        result = 'No Match'
        win = False

    net_gain = payout - bet_amount
    new_balance = current_balance + net_gain

    save_slots_history(bet_amount, slots, result, win, net_gain, new_balance, username)
    return slots, result, win, payout, new_balance

def save_slots_history(bet_amount, slots, result, win, net_gain, new_balance, username):
    path     = os.path.join(os.path.dirname(__file__), 'slots_results.csv')
    new_file = not os.path.exists(path)

    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['Username', 'Reel 1', 'Reel 2', 'Reel 3', 'Result', 'Bet Amount', 'Net Gain', 'Balance After'])
        w.writerow([
            username, slots[0], slots[1], slots[2], result, bet_amount, net_gain, new_balance
        ])