"""
Alex Kaplan
1/13/18

Implementation of a Blackjack card deck (multiple standard decks).
"""
from Deck.Deck import Deck

class BlackjackDeck(Deck):
    def __init__(self, n_decks):
        """
        Initialize a Deck for blackjack, consisting of cards from
        n_decks standard 52 card Decks.
        
        Args:
         :Int n_decks: Number of decks to include in the blackjack deck
        """
        # Initalize a Deck
        Deck.__init__(self)
        self.n_decks = n_decks
        # Extend the blackjack deck to consist of n_decks Decks of cards
        self._expand_deck()

    
    def _expand_deck(self):
        """
        Called on initialization and reset.
        Extend the deck to include each card n_decks times.
        """
        # There is a single deck by default. 
        # Create new cards n_decks-1 more times
        for i in range(self.n_decks-1):
            self.fill_deck()
    
    def reset_deck(self):
        """
        Override Deck method.

        Called when all cards have been used. 
        Reset the deck to n_decks * 52 shuffled cards.
        """
        self.fill_deck()
        self._expand_deck()
        self.shuffle()
