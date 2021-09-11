#!/usr/bin/env python3

# Written by Nathan Sinclair: Begun 10 Sep 2021
# Already learnt about shebang, ABC.@abstractmethods, git stage+commit+pull+push
# moderately overwhelmed (might equal learning)

from player_interface import LocalPlayerInterface
from ur_player import Board, Player
from random

# setup game
first_player = Player()
first_player.interface = LocalPlayerInterface()

second_player = Player(opponent=first_player)
second_player.interface = LocalPlayerInterface()

# Toss a coin for who goes first
curr_player = first_player
if random.randrange(2): 
    curr_player = curr_player.opponent

try:
    while not (board.player1_win or board.player2_win):
        roll = curr_player.interface.get_roll()
        if curr_player.can_move(roll):
            curr_player.interface.get_move(roll)
        else:
            curr_player.display
except GUIQuitException:
    pass
