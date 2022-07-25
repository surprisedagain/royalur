#!/usr/bin/env python3

# Written by Nathan Sinclair: Begun 10 Sep 2021
# Already learnt about shebang, ABC.@abstractmethods, git stage+commit+pull+push
# MVC approach appears to have been applied successfully1

from interface import LocalInterface, GUIQuitException
from player import Player
from random import randrange
from sys import exit

def play(*, no_click_roll = False):
    # setup game
    first_player = Player(LocalInterface(side = 'L'))
    second_player = Player(LocalInterface(side = 'R'), opponent=first_player)

    # Toss a coin for who goes first
    curr_player = first_player
    if randrange(2): 
        curr_player = second_player

    try:
        while not curr_player.opponent.has_won():
            another_move = True
            while another_move:
                roll = curr_player.roll_pyramids() 
                curr_player.interface.show_roll(roll, no_click_roll) # we have already rolled the dice before we show
                if not curr_player.can_move(roll):
                    curr_player.interface.show_cant_move()
                    another_move = False
                else:
                    # get valid move
                    start = curr_player.interface.get_start(roll)
                    end = start + roll
                    while not curr_player.is_valid_move(start, end):
                        curr_player.interface.show_invalid_move(start, end)
                        start = curr_player.interface.get_start(roll)
                        end = start + roll
                    # perform and show move
                    another_move, take = curr_player.move(start, end)
                    curr_player.interface.show_move(start, end)
                    if take:
                        curr_player.opponent.interface.show_taken()
            curr_player = curr_player.opponent
        curr_player.interface.show_lost()
        curr_player.opponent.interface.show_won()
        
        while True: # Wait for quit signal
            first_player.interface.check_for_quit()
            second_player.interface.check_for_quit()

    except GUIQuitException:
            first_player.interface.close()
            second_player.interface.close()
            exit(0)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Play the Royal Game of Ur")
    parser.add_argument('-ncr', '--noclickroll', action='store_true',
                                   help='do not require click to roll pyramids')
    options = parser.parse_args()
    play(no_click_roll=options.noclickroll)
