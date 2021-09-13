import pygame
import os
from abc import ABC

class PlayerInterface(ABC):

    @abstractmethod
    def show_roll(self, roll):
        pass

    @abstractmethod
    def get_move(roll):
        pass

    @abstractmethod
    def show_move(start, end):
        pass

    @abstractmethod
    def show_won(winner):
        pass

class LocalInterface(PlayerInterface):
    display = None

    def __init__ (self, side = 'L', num_pieces = 7):
        super().__init__()
        self._pieces_at_start = num_pieces

        if not LocalPlayerInterface.display:
            pygame.init()
            LocalInterface.clock = pygame.time.Clock()
            LocalInterface.display = pygame.display.set_mode((WIDTH, HEIGHT)) #arg? pygame.SCALED
            background = pygame.image.load(os.path.join('images',
                                                'background.PNG??')).convert()
            display.blit(background)

        if side == 'L':
            self._piece_surf = pygame.image.load(os.path.join('images', 'left_piece.PNG??')).convert()
           ????
           self._start_positions = [list of Rect]
           self._end_positions = [list of Rect]
           self._
           self._rollRect = Rect

            ???? set up the rects for places I can click: combat + my safe + roll box
            ???? also set positions for where I can move my pieces to and from
            rollRect, messageRect
            ???? square = squareRectList.index
        else: # side == 'R'
            ???? set up the rects for places I can click: combat + my safe + roll box
            ???? also set positions for where I can move my pieces to and from

        # put piece images into their 
        for i in range(self._pieces_at_start):
            self.display.blit((self._piece_surf, self._start_positions[i]))

    def get_move(self, roll):
        pygame wait for click on some square and return INDEX of containing Rect

    def show_roll(self, roll):
        pygame clear my rollRect
        pygame wait for click on rollRect
        pygame show roll in rollRect

    def show_move(self, start, end):
        pass

    def show_cant_move(self):
        pygame show cant move message in messageRect


    def show_invalid_move(self, start, end):
        pygame flash start and end rect

    def show_won(self):
        if not LocalPlayerInterface.result_shown:
            pygame show won message
            LocalPlayerInterface.result_shown = True

    def show_lost(self):
        if not LocalPlayerInterface.result_shown:
            pygame show lost message
            LocalPlayerInterface.result_shown = True

    def check_for_quit():
        pygame clear all events in event queue
        if QUIT:
            raise GUIQuitException

    def close(self):
        if self.display:
            pygame close display
            self.display = None

#class RemotePlayerInterface(PlayerInterface):
#   pass
