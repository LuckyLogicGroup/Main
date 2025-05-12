import random, os, csv

def determine_winner(user_choice, bet_amount, current_balance, username):
    computer_choice = random.choice(['🪨', '📄', '✂️'])

    # Determine game result
    if user_choice == computer_choice:
        result = "Draw"
        net_gain = 0
    elif (user_choice == '🪨' and computer_choice == '✂️') or \
         (user_choice == '📄' and computer_choice == '🪨') or \
         (user_choice == '✂️' and computer_choice == '📄'):
        result = "Win"
        net_gain = bet_amount * 3
    else:
        result = "Loss"
        net_gain = 0

    # Balance updates
    new_balance = current_balance - bet_amount + net_gain

    # Save to CSV
    save_rps_history(user_choice, computer_choice, result, bet_amount, net_gain - bet_amount, new_balance, username)

    return result, computer_choice, net_gain - bet_amount, new_balance

def save_rps_history(user_choice, computer_choice, result, bet_amount, net_gain, new_balance, username):
    path = os.path.join(os.path.dirname(__file__), 'rps_results.csv')
    new_file = not os.path.exists(path)

    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow([
                'Username', 'User Choice', 'Computer Choice',
                'Result', 'Bet Amount', 'Net Gain', 'Balance After'
            ])
        writer.writerow([
            username, user_choice, computer_choice,
            result, bet_amount, net_gain, new_balance
        ])
