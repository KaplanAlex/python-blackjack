"""
Wove Programming Exercise - Blackjack
Alex Kaplan
1/13/18

Implementation of a deck of cards.
"""

import random

from Deck.Card import Card

class Deck:
    def __init__(self):
        """
        Instantiate a deck of 52 cards (unshuffled).
        """
        self.cards = []
        self.fill_deck()

    def fill_deck(self):
        """
        Create all 52 cards present in a standard deck and append them
        to the internal set.
        """
        # Valid suit names
        suits = ["Diamonds", "Hearts", "Clubs", "Spades"]

        # Add a card from each suit for all numbers 2-10
        for card_val in range(2, 11):
            for suit in suits:
                new_card = Card(suit, str(card_val))            
                self.cards.append(new_card)

        # Add all face cards
        faces = ["Jack", "Queen", "King", "Ace"]
        for face in faces:
            for suit in suits:
                new_card = Card(suit, face)
                self.cards.append(new_card)

    def shuffle(self):
        """
        Randomize the order of the cards in the deck
        """
        random.shuffle(self.cards)

    def reset_deck(self):
        """
        Reset the deck to 52 shuffled cards.
        """
        self.fill_deck()
        self.shuffle()
    
    def draw(self):
        """
        Draw a card from the top of the deck
        Return the card and remove it from the deck
        """
        # Reset the deck if you run out of cards.
        if len(self.cards) == 0:
            self.reset_deck()
        
        # Return a card from the deck.
        return self.cards.pop()

    def get_num_cards(self):
        """
        Return number of cards remaining in the deck.
        """
        return len(self.cards)

    def print_deck(self):
        """
        Print the cards in the deck.
        """
        for card in self.cards:
            card.print_card()
