#!/usr/bin/env python3

# Written by Nathan Sinclair: Begun 10 Sep 2021
# Already learnt about shebang, ABC.@abstractmethods, git stage+commit+pull+push
# moderately overwhelmed (might equal learning)

from ur_interface import LocalPlayerInterface
from ur_player import Player
from random import randrange

# setup game
first_player = Player(LocalPlayerInterface(side = 'L'))
second_player = Player(LocalPlayerInterface(side = 'R'), opponent=first_player)

# Toss a coin for who goes first
curr_player = first_player
if randrange(2): 
    curr_player = second_player

try:
    while not curr_player.opponent.has_won():
        another_move = True
        while another_move:
            roll = curr_player.roll_pyramids() 
            curr_player.interface.show_roll(roll) # we have already rolled the dice before we show
            if not curr_player.can_move(roll):
                curr_player.interface.show_cant_move(roll)
                # another_move remains True
            else:
                # get valid move
                end = curr_player.interface.get_move(roll)
                start = end - roll
                while not curr_player.is_valid_move(start, end):
                    curr_player.interface.show_invalid_move(start, end)
                    end = curr_player.interface.get_move(roll)
                    start = end - roll
                # perform and show move
                another_move = curr_player.move(start, end)
                curr_player.interface.show_move(start, end)
    curr_player.interface.show_lost()
    curr_player.opponent.interface.show_won()
    
#
    # Wait for quit signal
    while True:
        first_player.interface.check_for_quit()
        second_player.interface.check_for_quit()

except GUIQuitException:
        first_player.interface.quit()
        second_player.interface.quit()
