# main.py

import deck
import probability
import stats

def display_menu():
    """Display the main menu options."""
    print("\n===== Card Game Menu =====")
    print("1. Show Standard Deck of Cards")
    print("2. Probability Challenge")  # Now shows probability of a specific card
    print("3. Percentage Calculator")   # Now allows calculation of percentage
    print("4. Show Statistics")
    print("0. Exit")

def main():
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice: ")
            
            if choice == '1':
                deck.show_standard_deck()
            elif choice == '2':
                probability.probability_challenge()  # This now shows the probability of a specific card
            elif choice == '3':
                stats.calculate_percentage_probability()  # This now handles percentage calculations
            elif choice == '4':
                stats.show_stats()
            elif choice == '0':
                print("Exiting the program...")
                break
            else:
                print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            


if __name__ == "__main__":
    main()