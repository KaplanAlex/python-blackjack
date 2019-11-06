"""
Alex Kaplan
1/13/18

Representation of a Blackjack player
"""

from Game.Hand import Hand

class Player:
    def __init__(self, name):
        """
        Initialize a blackjack player
        Args:
         :String name: Player's name
        """
        self.name = name
        self.money = 1000           # All players start with $1000.
        self.hands = []             # Cards the player holds (could have multiple hands).
        self.initial_bet = 0        # Amount the player is betting on their hand.

    def reset(self):
        """
        Called prior to the start of a new hand. Reset the user's hand.
        """
        self.hands = []

    def first_deal(self, card):
        """
        Called when initially dealing to a player. Places all cards in a
        single (first hand)
        Args:
         :Card card: Card object added to the player's hand.
        """
        # This is the first card delt to the player
        if len(self.hands) == 0:
            hand = Hand(self.initial_bet)
            self.hands.append(hand)
        else:
            hand = self.hands[0]
        self.deal_card(card, hand)
        self.print_hands()
        
    def show_hand(self, h_idx):
        """
        Show all of the cards in a hand.
        Args:
         :Int h_idx: Index of the hand
        """
        self.hands[h_idx].show_cards()


    def score_first(self):
        """
        Return the score of only the first hand.
        Useful for the general player who only has one hand.
        """
        return self.hands[0].score_hand()

    def deal_card(self, card, hand):
        """
        Deal a card to one of the player's hands.
        Args:
         :Card card: Card object added to the player's hand.
         :Hand hand: The Hand to deal the card to.
        """        
        hand.add_card(card)

    def print_hands(self):
        """
        Print the player's hand.
        """
        print(self.name + "\'s Hand:")
        if len(self.hands) > 1:
            for i in range(len(self.hands)):
                print('Hand ' + str(i) + ':')
                self.hands[i].print_hand()
        else:
            self.hands[0].print_hand()
    
    def prompt_initial_bet(self):
        """
        Prompt the user to make a bet at the start of the round
        """
        # Iterate until the player places and confirms a valid bet.
        confirmed = False
        while not confirmed:
            bet_str = self.name + " what is your initial bet? You have $" + str(self.money)
            bet_str += " (Enter an integer value): "
            bet_amount = input(bet_str)
            
            # Ensure the player's bet is valid and meets the minimum bet amount ($0)
            while not bet_amount.isdigit() or int(bet_amount) < 0:
                print("ERROR: Invalid Input") 
                print("You must bet a non-negative integer value")
                bet_amount = input(bet_str)
            bet_amount = int(bet_amount)

            # Ensure the player has enough money to make the bet
            if bet_amount > self.money:
                print("You don't have enough money to make that bet. You have $" + str(self.money))
                continue

            # Confirm the bet
            confirm_str = ''
            while confirm_str.lower() != 'y' and confirm_str.lower() != 'n':
                confirm_str = input("Bet $" + str(bet_amount) + "? (Y to confirm, N to cancel): ")
            
            if confirm_str.lower() == 'y':
                confirmed = True
            else:
                print("Bet cancelled")
        
        # Place the bet
        self.money -= bet_amount
        self.initial_bet = bet_amount
        print(self.name + " bet $" + str(self.initial_bet) + '.\n')


    def start_turn(self, game_deck):
        """
        Manages a player's turn
        Args:
         :Deck game_deck: Deck used in the blackjack game 
            used to draw additional cards. 
        """
        print(str(self.name) + "\'s turn")
        
        # Play through all hands as they are generated
        h_idx = 0
        while h_idx < len(self.hands):
            # play_hand returns True if a hand is split. 
            # This replaces the hand at h_idx. 
            # Replay this index until it isn't split.
            while self.play_hand(game_deck, h_idx):
                continue
            
            # Move on to the next hand
            h_idx += 1

    def manage_split(self, game_deck, h_idx):
        """
        Manage splitting a hand at the start of the hand's plathrough.
        Args:
         :Deck game_deck: Deck used in the blackjack game 
            used to draw additional cards. 
         :Int h_idx: Index of the hand to play through.
        
        Return:
            Bool - True if hand was split
        """
        hand = self.hands[h_idx]
        # Each hand starts with two cards. If they are equal, the player can split them and double their bet.
        if hand.get_bet() <= self.money:
            if hand.get_first().int_value() == hand.get_second().int_value():
                print('Both cards in this hand have equal value, would you like to split?')
                print('You must place your original bet amount on the second hand.')
                
                # Prompt to split their hand.
                split_str = ''
                while split_str.lower() != 'y' and split_str.lower() != 'n':
                    split_str = input('Press Y to split and N to continue: ')

                # Confirm the split.
                if split_str.lower() == 'y':
                    confirm_str = ''
                    while confirm_str.lower() != 'y' and confirm_str.lower() != 'n':
                        confirm_str = input('Are you sure you want to split (Y to split, N to cancel): ')
                    
                    # Split the hand
                    if confirm_str.lower() == 'y':
                        self.money -= hand.get_bet()
                        print(self.name, 'bet another $', hand.get_bet(),'and split their hand!\n')
                        
                        # Create a new hand from the first card
                        first_card = hand.get_first()
                        first_new = Hand(hand.get_bet())
                        first_new.add_card(first_card)
                        first_new.add_card(game_deck.draw())
                        self.hands[h_idx] = first_new

                        # Create a second hand from the second card
                        second_card = hand.get_second()
                        second_new = Hand(hand.get_bet())
                        second_new.add_card(second_card)
                        second_new.add_card(game_deck.draw())
                        self.hands.insert(h_idx+1, second_new)

                        # Print the new hands
                        self.print_hands()
                        
                        return True
                        
        return False

    def manage_double_down(self, game_deck, hand):
        """
        Manage presentation of double down option to the user
        Args:
         :Deck game_deck: Current deck used in the blackjack Game.
         :Hand hand: The hand the player has the opportunity to double down on.
        
        Return:
         True on Double Down, Else False
        """
        # Allow the player to double down at the start of their turn with this hand if 
        # they have enough money.
        if self.money >= hand.get_bet():
            dd_string = "Press (D) to double down (double your initial bet and receive " 
            dd_string += "only one additional card).\nPress any other key to continue: "
            double_decision = input(dd_string)
            
            # Double down!
            if double_decision.lower() == 'd':
                confirm_str = ''
                while confirm_str.lower() != 'y' and confirm_str.lower() !=  'n':
                    confirm_str = input('Are you sure you want to double down (Y to confirm, N to Cancel): ')

                # If they double down, they double their bet and get one more card.
                if confirm_str.lower() == 'y':
                    self.money -= hand.get_bet()
                    hand.double_bet()

                    print(self.name, 'doubled their bet to $' + str(hand.get_bet()) + '!\n')
                    self.deal_card(game_deck.draw(), hand)
                    
                    # Display the hand with the new card.
                    print('New hand:')
                    hand.print_hand()

                    # Inform user of interesting events.
                    dd_score = hand.score_hand()
                    if dd_score == 21:
                        print(self.name, 'got Blackjack!\n')
                    elif dd_score > 21:
                        print(self.name, 'busted...\n')
                    
                    # Turn ends after 1 additional card.
                    return True
                else:
                    print(self.name, 'cancelled their decision to double down.')
        else:
            print(self.name, 'does not have enough money to double down.')
        
        # Player did not double down.
        return False

    def play_hand(self, game_deck, h_idx):
        """
        Have the player play through a hand.
        Args:
         :Deck game_deck: Deck used in the blackjack game 
            used to draw additional cards. 
         :Int h_idx: Index of the hand to play through.
        
        Returns True on a hand split. False otherwise.
        """
        # Output for multiple hands
        if len(self.hands) > 1:
            print("\nContinuing", str(self.name) + '\'s', "turn")
            print("Playing hand", str(h_idx) + ":")
        
        hand = self.hands[h_idx]
        hand_score = hand.score_hand()
        print('\nCurrent hand:')
        hand.print_hand()

        # The hand is complete if it reached blackjack.
        if hand_score == 21:
            print(self.name, 'got Blackjack! \n')
            return False

        # Allow the player to split their hand if they have two cards of the same
        # value and enough money to double their bet.
        if self.manage_split(game_deck, h_idx):
            # Return to playthrough the new hand which replaced self.hands[h_idx]
            return True
        
        # # Allow the player to double down at the start of their turn with this hand if 
        # # they have enough money.
        if self.manage_double_down(game_deck, hand):
            # The player chose to double down. Their turn is over.
            return False
        
        # Loop until the player gets blackjack, busts, or chooses to stay
        while True:
            decision = input("Would you like to stay (S) or hit (H)?: ")
            while decision.lower() != 's' and decision.lower() != 'h':
                print("ERROR: Invalid input")
                print("Please enter an \"s\" to stay and a \"h\" to hit (take a card)")
                decision = input("Would you like to stay (S) or hit (H)?: ")

            # Chose to stay.
            if decision.lower() == 's':
                print("")
                print(self.name, "chose to stay.\n")
                return False

            # Chose to hit.
            if decision.lower() == 'h':
                print("")
                if (len(self.hands) > 1):
                    print(self.name, "continues playing hand", str(h_idx))
                
                # Take another card and show the updated hand
                self.deal_card(game_deck.draw(), hand)
                print('Current Hand:')
                hand.print_hand()
            
            # Their turn is over if they have blackjack.
            new_score = hand.score_hand()
            if new_score == 21:
                print(self.name, 'got Blackjack!\n')
                return False
    
            # or if they bust.
            elif new_score > 21:
                print(self.name, "busted...\n")
                return False

    def reward(self, dealer_score):
        """
        Determine if the player won the hand and update the amount of money
        they have to reflect this outcome.
        """
        if len(self.hands) > 1:
            print(self.name, 'split their hand and ended up with', len(self.hands), 'hands!')

        self.print_hands()

        # Compute the reward for each hand.
        for h_idx in range(len(self.hands)):
            hand = self.hands[h_idx]
            # When multiple hands exist, inform the player's which hand is being scored.
            if len(self.hands) > 1:
                print('Scoring', str(self.name) + '\'s hand ' + str(h_idx) + '.')
                hand.print_hand()
            
            multiplier = hand.compute_reward(dealer_score)
            winnings = int(multiplier*(hand.get_bet()))
            self.money += winnings

            # Print win message
            if multiplier:
                # Tie.
                if multiplier == 1:
                    print(self.name, 'tied the dealer, their bet of $' + str(hand.get_bet()) + ' was returned.')
                # Win
                else:
                    print(self.name, 'beat the dealer! They made $' + str(winnings - hand.get_bet()), 'from a bet of $' + str(hand.get_bet()))
                    # Blackjack
                    if multiplier == 2.5:
                        print('Blackjack has a 1.5x payout!')
            
            # Print loss message
            else:
                print(self.name, 'lost a bet of $' + str(hand.get_bet()))
            print(self.name, 'now has $' + str(self.money) + '.\n')

        # Delete the bet amount
        self.initial_bet = 0

    def get_money(self):
        """
        Return the amount of money the player has
        """
        return self.money