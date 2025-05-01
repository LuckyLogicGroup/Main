# stats.py

import csv
from datetime import datetime
import os

def save_result(difficulty_level, question_type, correct, user_answer, correct_answer, attempts_used):
    """Save the result to a CSV file."""
    filename = 'probability_challenge_results.csv'
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers if the file is new
        if not file_exists:
            writer.writerow(['Timestamp', 'Difficulty', 'Question Type', 
                             'Correct', 'User Answer', 'Correct Answer',
                             'Attempts Used'])
        
        # Write the result
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            f'Level {difficulty_level}',
            question_type,
            'Correct' if correct else 'Incorrect',
            user_answer,
            correct_answer,
            attempts_used
        ])
def calculate_percentage_probability():
    """Calculate percentage probabilities with 3 tries."""
    print("\nWelcome to the Percentage Probability Calculator!")
    print("You can calculate the percentage probability of drawing a specific card or suit.")
   
    choice = input("Do you want to calculate for a specific (1) card or (2) suit? ")
    max_tries = 3
    correct = False

    if choice == '1':
        card_value = input("Enter card value (e.g., 'Ace', 'King'): ").strip()
        correct_percentage = (4 / 52) * 100  # 4 Aces in a standard deck
        tries_used = 0

        while tries_used < max_tries and not correct:
            tries_used += 1
            try:
                user_input = input(f"Attempt {tries_used}: Enter your probability percentage (e.g., '7.69'): ")
                user_percentage = float(user_input)

                if abs(user_percentage - correct_percentage) < 0.01:
                    print("🎉 Correct! 🎉")
                    correct = True
                else:
                    print("❌ Incorrect! Try again.")
            except ValueError:
                print("Please enter a valid percentage.")
                tries_used -= 1  # Don't count invalid inputs as a try

        if not correct:
            print(f"The correct answer was {correct_percentage:.2f}%.")
    elif choice == '2':
        suit = input("Enter suit (Hearts, Diamonds, Clubs, Spades): ").strip()
        correct_percentage = (13 / 52) * 100  # 13 cards in each suit
        tries_used = 0

        while tries_used < max_tries and not correct:
            tries_used += 1
            try:
                user_input = input(f"Attempt {tries_used}: Enter your probability percentage (e.g., '25'): ")
                user_percentage = float(user_input)

                if abs(user_percentage - correct_percentage) < 0.01:
                    print("🎉 Correct! 🎉")
                    correct = True
                else:
                    print("❌ Incorrect! Try again.")
            except ValueError:
                print("Please enter a valid percentage.")
                tries_used -= 1  # Don't count invalid inputs as a try

        if not correct:
            print(f"The correct answer was {correct_percentage:.2f}%.")
    else:
        print("Invalid choice.")
        return



def save_result(difficulty_level, question_type, correct, user_answer, correct_answer, attempts_used):
    """Save the result to a CSV file in the same folder as this script."""
    filename = os.path.join(os.path.dirname(__file__), 'probability_challenge_results.csv')
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers if the file is new
        if not file_exists:
            writer.writerow(['Timestamp', 'Difficulty', 'Question Type', 
                             'Correct', 'User Answer', 'Correct Answer',
                             'Attempts Used'])
        
        # Write the result
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            f'Level {difficulty_level}',
            question_type,
            'Correct' if correct else 'Incorrect',
            user_answer,
            correct_answer,
            attempts_used
        ])
