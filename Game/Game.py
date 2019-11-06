"""
Alex Kaplan
1/13/18

Manager of Blackjack Game. 
Follows all standard blackjack rules, excluding insurance and surrendering.
Allows players to:
 - Double Down on their first hand 
    If the player has enough money to double their bet.
 - Split Hand on first move per hand (potential for recursive splitting of split hands)
    If the hand consists of two cards of the same value.
 - Choose to stay on a hand at any time, or hit until they stay or bust.
"""

from Deck.BlackjackDeck import BlackjackDeck
from Game.Player import Player

class Game:
    def __init__(self, player_names, n_decks):
        """
        Initialize a blackjack player
        Args:
        :List player_names: Names of participants in the blackjack game.
        :Int n_decks: Number of decks cards are drawn from (Standard 
            games include 1-8 decks).
        """
        self.player_names = player_names
        
        # People playing the game
        self.players = []
        self.init_players()

        # Dealer hand
        self.dealer = Player("Dealer")

        # Initialize a deck containing n_decks standard 52 card decks.
        self.deck = BlackjackDeck(n_decks)
        
        # Start the blackjack game
        self.run_game()

    def init_players(self):
        """
        Create player objects for each player name
        """
        for name in self.player_names:
            new_player = Player(name)
            self.players.append(new_player)

    def run_game(self):
        """
        Run through rounds of blackjack until all players leave or 
        run out of money.
        """
        # Randomize the card order to start the game.
        self.deck.shuffle()
        
        # Continue dealing to the existing players until all players have left.
        while len(self.players) > 0:
            # Place initial bets and deal two cards to each player
            self.start_round()

            # Allow players to take more cards until they stay or bust
            self.play_hands()

            # Play through the dealer's hand
            self.play_dealer()
            
            # Reward winning hands
            self.reward()

            # Ask players if they want to play another hand
            self.prompt_continue()
        
        # No players remain - end of game.
        print('All players have left the table. The game has ended.\n\n\n')

    def start_round(self):
        """
        Start a new round.
        """
        # Start by prompting each player to make a bet.
        for player in self.players:
            player.prompt_initial_bet()
            # Clear player's old hand(s)
            player.reset()
        self.dealer.reset()

        # Deal two cards to every player
        print('\nDealing Cards...')
        for i in range(2):
            # All players get a card
            for player in self.players:
                player.first_deal(self.deck.draw())

            # The dealer gets two cards, but the first card is hidden.
            dealer_card = self.deck.draw()
            if i == 0:
                dealer_card.hide()
            self.dealer.first_deal(dealer_card)

    def play_hands(self):
        """
        Prompt each player to play through their hand.
        """
        print("Now each player will play their hand")
        for player in self.players:
            player.start_turn(self.deck)

    def play_dealer(self):
        """
        Expose the dealer's hidden card and play through the dealer's hand
        House rules are the dealer must:
            1. Hit until 17
            2. Must stay after 17
        """
        print('--------------------------------------------------------------')
        print('All players have played their hands, now the dealer will play.')
        # Reveals the first card (hidden)
        self.dealer.show_hand(0)
        self.dealer.print_hands()

        # The dealer hits until its score exceeds 17
        while self.dealer.score_first() < 17:
            print('The Dealer takes another card.\n')
            self.dealer.first_deal(self.deck.draw())

        if self.dealer.score_first() > 21:
            print('The dealer busted...\n')
        elif self.dealer.score_first() == 21:
            print('The dealer got blackjack!\n')
        else:
            print('Dealer\'s final score is:', self.dealer.score_first(), "\n")
    
    def reward(self):
        """
        Once all players' hands have been played and the dealer
        has followed the house rules, winning hands are rewarded.
        """
        dealer_score = self.dealer.score_first()
        
        for player in self.players:
            # Update the player to reflect a win or loss based on the dealer_score
            player.reward(dealer_score)

    def prompt_continue(self):
        """
        Called at the end of each round.
        Ask each player if they want to leave the game or keep playing.
        Player's with no money must leave
        """
        player_exit = []
        for p_idx in range(len(self.players)):
            player = self.players[p_idx]
            # The player has no money. They can't keep playing
            if player.get_money() <= 0:
                print(player.name, "has no money left, they leave the table.\n")
                player_exit.append(p_idx)
            else:
                keep_playing = ''
                while keep_playing.lower() != 'y' and keep_playing.lower() != 'n':
                    continue_msg = str(player.name) + ", would you like to keep playing?" 
                    continue_msg += " You have $" + str(player.get_money()) + ". (Y to play again, N to leave): "
                    keep_playing = input(continue_msg)
                if keep_playing.lower() == 'y':
                    print(player.name, "stayed.\n")
                else:
                    print(player.name, "left with $" + str(player.get_money()) + '.\n')
                    player_exit.append(p_idx)
        
        # Remove all players that exited.
        # Reverse player_exit so that the largest indices are popped first.
        # Smaller indices will still point to the correct player after larger indices are popped.
        player_exit.reverse()
        for p_idx in player_exit:
            # Removing each p
            self.players.pop(p_idx)
        