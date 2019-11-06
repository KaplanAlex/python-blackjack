"""
Alex Kaplan
1/13/18

Representation of a playing card.
"""


class Card:
    def __init__(self, suit, value):
        """
        Initialize a card 
        Args:
         :String suit: Card's suit - Diamonds, Hearts, Spades, Clubs
         :String value: Card value as a String - # 2-10, Jack, Queen, King, Ace
        """
        self.suit = suit
        self.value = value
        self.hidden = False     # Prevents the value form being printed or scored.

    def print_card(self):
        """
        Print the card
        """
        if self.hidden:
            print('Hidden Card')
        else:
            print(self.value, "of", self.suit)

    def hide(self):
        """
        Hide the value of a card so that it wont be displyed
        """
        self.hidden = True
    
    def show(self):
        """
        Set a card to visible
        """
        self.hidden = False

    def int_value(self):
        """
        Integer value of the card
        """
        # Number
        if self.value.isdigit():
            return int(self.value)
        # Ace
        elif self.value == 'Ace':
            return 11
        # Face card
        return 10