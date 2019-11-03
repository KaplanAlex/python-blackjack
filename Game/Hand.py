"""
Wove Programming Exercise - Blackjack
Alex Kaplan
1/13/18

Representation of a hand. Player's can have
multiple hands following a decision to split
their initial hand.
"""
from Deck.Card import Card

class Hand:
    def __init__(self, bet_amount):
        """
        Initialize an empty hand.
        All hands have an associated bet
        Args:
         :Int bet_amount: Amount the player bets on this hand
        """
        self.cards = []
        self.bet_amount = bet_amount

    def add_card(self, card):
        """
        Add a card to the hand
        Args:
         :Card card: The Card object to be added
        """
        self.cards.append(card)

    def get_bet(self):
        """
        Return the amount bet on the hand
        """
        return self.bet_amount

    def double_bet(self):
        """
        Called when the player chooses to double down
        on this hand (Sufficient money is validated elsewhere). 
        
        Double the bet amount.
        """
        self.bet_amount *= 2

    def get_first(self):
        """
        Return the first card. Used to split the hand
        """
        if len(self.cards) == 0:
            print('Error: Not enough cards!')
        return self.cards[0]

    def get_second(self):
        """
        Return the second card. Used to split the hand
        """
        if len(self.cards) < 2:
            print('Error: Not enough cards!')
        return self.cards[1]

    def print_hand(self):
        """
        Print the cards in the hand.
        """
        for card in self.cards:
            card.print_card()
        
        # Score the hand. Hands with hidden cards will return -1
        hand_score = self.score_hand()
        
        # Only print the score for hands with no hidden cards.
        if hand_score > 0:
            print("Score: ", hand_score)

        print("\n")
    
    def show_cards(self):
        """
        Ensures no cards are hidden
        """
        for card in self.cards:
            card.show()

    def score_hand(self):
        """
        Compute the score of the player's hand
        Return the player's score, -1 if any cards are hidden.
        """
        score = 0
        for card in self.cards:
            if card.hidden:
                return -1
            score += card.int_value()

        # Go back through and reduce Ace values as needed
        for card in self.cards:
            if score <= 21:
                break
            # Reduce the Ace value to 1 to lower high score
            if card.value == 'Ace':
                score -= 10
        
        return score
    
    def compute_reward(self, dealer_score):
        """
        Compute the player's winnings given the dealer's score
        Args:
         :Int dealer_score: The score of the dealer's hand.
        
        Return: 
         :Int Earnings multiplier:
            0 for loss
            1 for tie
            2 for win
            2.5 for blackjack
        """
        hand_score = self.score_hand()

        # Amount the bet is multiplied by. Defaults to 0 for a loss
        multiplier = 0
        
        # Player always loses if its score exceeds 21 (even if the dealer busts)
        if hand_score > 21:
            multiplier = 0
        
        # Dealer busts, so the player wins
        elif dealer_score > 21:
            # Bet is doubled on win.
            multiplier = 2
            # Blackjack pays out 1.5 times + original bet.
            if hand_score == 21:
                multiplier = 2.5
                            
        # No one bust
        # Tie. Return the bet amount.
        elif hand_score == dealer_score:
            multiplier = 1

        # Player's score beats dealers.
        elif hand_score > dealer_score:
            # Bet is doubled on win.
            multiplier = 2
            # Blackjack has 1.5x payout + original bet.
            if hand_score == 21:
                multiplier = 2.5
        
        return multiplier
        