# probability.py

import csv
from fractions import Fraction
from deck import create_standard_deck
from stats import save_result

def probability_challenge():
    """Main function for the probability challenge."""
    deck = create_standard_deck()
    total_cards = 52
    max_tries = 3

    print("Welcome to the Probability Challenge!")
    print("Select your option:")
    print("1. Probability for a specific card (e.g., 'Ace')")
    print("2. Probability for a specific suit (e.g., 'Hearts')")
    print("3. Probability for a specific card and suit (e.g., 'Ace of Hearts')")

    choice = input("Enter your choice (1-3): ")
    
    correct_probability = None
    question_type = ""
    
    if choice == '1':
        value = input("Enter card value (2-10, Jack, Queen, King, Ace): ").strip()
        correct_probability = Fraction(4, total_cards)  # 4 of each value
        question_type = f"Probability for {value}"
    elif choice == '2':
        suit = input("Enter suit (Hearts, Diamonds, Clubs, Spades): ").strip()
        correct_probability = Fraction(13, total_cards)  # 13 cards in each suit
        question_type = f"Probability for {suit}"
    elif choice == '3':
        card_input = input("Enter card (e.g., 'Ace of Hearts'): ").strip()
        correct_probability = Fraction(1, total_cards)  # 1 specific card
        question_type = f"Probability for {card_input}"
    else:
        print("Invalid choice.")
        return

    correct = False
    for attempt in range(max_tries):
        tries_used = attempt + 1
        user_input = input(f"Attempt {tries_used}: Enter your answer in fraction form (e.g., '4/52'): ")
        
        try:
            user_probability = Fraction(user_input)
            if user_probability == correct_probability:
                print("🎉 Correct! 🎉")
                correct = True
                break
            else:
                print("❌ Incorrect! Try again.")
        except ValueError:
            print("Please enter a valid fraction (e.g., '4/52').")
    
    if not correct:
        print(f"The correct answer was {correct_probability}.")

    # Save the result to CSV
    save_result(
        difficulty_level=1,  # Adjust as needed
        question_type=question_type,
        correct=correct,
        user_answer=str(user_probability) if correct else user_input,
        correct_answer=str(correct_probability),
        attempts_used=tries_used
    )