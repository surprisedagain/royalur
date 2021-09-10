import player_interface
from ur_board import Board

# setup game
curr_player = LocalPlayerInterface()
other_player = LocalPlayerInterface(player1.screen)
board = Board()

# Toss a coin for who goes first
if random.randrange(2): 
    curr_player, other_player = other_player, curr_player

while not (board.player1_win or board.player2_win):
    roll = curr_player.get_roll()
    if curr_player.can_move(roll):
        curr_player.interface.get_move(roll)
    else:
        curr_player.display
