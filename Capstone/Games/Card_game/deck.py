# deck.py

import random
from card import Card

def create_standard_deck():
    """Create a standard 52-card deck."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 
              'Jack', 'Queen', 'King', 'Ace']
    
    deck = [Card(suit, value) for suit in suits for value in values]
    return deck

def show_standard_deck():
    """Display all cards in a standard deck."""
    deck = create_standard_deck()
    
    print("Standard Deck of 52 Cards:")
    print("-------------------------")
    
    for card in deck:
        print(card)
    
    print(f"\nTotal number of cards: {len(deck)}")