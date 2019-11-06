"""
Alex Kaplan
1/13/18

Driver for Blackjack program.
"""
from Game.Game import Game

def new_game_sequence():
    """
    Prompt the user with the input necessary to initialize a game.
    Number of players, player names, and number of standard 52 card decks.
    """
    print("\n-------------------- Welcome to Blackjack --------------------")

    n_players = input("How many people are playing? (Enter an integer value): ")
    
    # Prompt the user for valid input (Must be an integer > 0)
    while not n_players.isdigit() or int(n_players) < 1:
        print("ERROR: Invalid Input") 
        print("The number of players must be expressed as a positive integer value ")
        n_players = input("How many people will be playing?: ")
    n_players = int(n_players)

    # Get the player's names
    print('Please enter each players name')
    player_names = []
    for i in range(n_players):
        new_player = input("Player " + str(i+1) + "\'s name: ")
        while len(new_player) == 0:
            print('ERROR: Player name must have at least one character')
            new_player = input("Player " + str(i+1) + "\'s name: ")
        player_names.append(new_player)

    # Get user input dictating the number of decks to use
    n_decks = input("How many decks would you like to use? Standard blackjack uses between 1 and 8 decks: ")
    
    # Prompt the user for valid input (Must be an integer > 0)
    while not n_decks.isdigit() or int(n_decks) < 1:
        print("ERROR: Invalid Input") 
        print("The number of decks must be expressed as a positive integer value")
        n_decks = input("How many decks should be included?: ")
    n_decks = int(n_decks)

    print("Starting a new game with", n_players, "players and", n_decks, "decks (" + str(n_decks*52) + " cards)")
    print(".\n.\n.\n.\n")
    
    # Create a blackjack game with this information.
    blackjack_game = Game(player_names, n_decks)
    
if __name__ == '__main__':
    # Continuinly restart the game after each exit until the program is terminated.
    while True:
        new_game_sequence()

    

