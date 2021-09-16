import pygame
import os
from random import shuffle
from abc import ABC

class GUIQuitException(Exception):
    pass

class PlayerInterface(ABC):

    @abstractmethod
    def show_roll(self, roll):
        pass

    @abstractmethod
    def get_start(self, roll):
        pass

    @abstractmethod
    def show_move(start, end):
        pass

    @abstractmethod
    def show_cant_move(start, end):
        pass

    @abstractmethod
    def show_invalid_move(start, end):
        pass

    @abstractmethod
    def show_won(winner):
        pass

class LocalInterface(PlayerInterface):
    dirname = os.path.dirname(__file__) # directory of this module's file
    background_s = pygame.image.load(os.path.join(dirname, 'images',
                                                  'background.PNG??')).convert()
    pyramid0_s = pygame.image.load(os.path.join(dirname, 'images',
                                                  'pyramid0.PNG??')).convert()
    pyramid1_s = pygame.image.load(os.path.join(dirname, 'images',
                                                  'pyramid1.PNG??')).convert()

    pygame.init()
    pygame.event.set_blocked(None) # block all events
    pygame.event.set_allowed(tuple(pygame.QUIT, pygame.MOUSEBUTTONDOWN))

    clock = pygame.time.Clock()
    window = pygame.display.set_mode((WIDTH, HEIGHT)) #arg? pygame.SCALED ????


    def __init__ (self, side = 'L', num_start_pieces = 7, num_end_pieces = 0):
        self._num_start_pieces = num_start_pieces
        self._num_end_pieces = num_end_pieces

        if side == 'L':
            self._piece_s = pygame.image.load(
                                  os.path.join(
                                    self.dirname, 'images', 'left_piece.PNG??'
                                  )
                                ).convert() #???? look into alpha-convert
            self._start_rects = () #???? Tuple of Rect
            self._end_rects = () #???? Tuple of Rect
            self._board_squares = () #???? Tuple of Rect
            self._roll_rects = () #???? Tuple of Rect
            self._message_rect = pygame.Rect(0, 0, 0, 0) #???? Rect

        else: # side == 'R'
            self._piece_s = pygame.image.load(
                                  os.path.join(
                                    self.dirname, 'images', 'right_piece.PNG??'
                                  )
                                ).convert() #???? look into alpha-convert
            self._start_rects = () #???? Tuple of Rect
            self._end_rects = () #???? Tuple of Rect
            self._board_squares = () #???? Tuple of Rect
            self._roll_rects = () #???? Tuple of Rect
            self._message_rect = pygame.Rect(0, 0, 0, 0) #???? Rect

        self._start_area = self._start_rects[0].unionall(self._start_rects[1:])
        self._roll_area = self._roll_rects[0].unionall(self._roll_rects[1:])
        self._board_area = \
                        self._board_squares[0].unionall(self._board_squares[1:])

        self.window.blit(self.background)
        # put piece images into their initial positions
        self.window.blits(tuple((self._piece_s, rect)
                    for rect in self._start_rects[:self._num_start_pieces]))
        self.clock.tick(40)
        pygame.display.flip()

    @classmethod
    def get_next_matching_event(cls, *event_types):
        while True:
            event = pygame.event.wait()
            if event.type in event_types:
                return event
            if event.type == pygame.QUIT:
                raise GUIQuitException

    def show_roll(self, roll):
        pyramids = [self.pyramid1_s] * roll + [self.pyramid0_s] * (4 - roll)
        pyramids.shuffle()
        while True: # wait until BUTTONDOWN in _roll_area
            event = self.get_next_matching_event(pygame.MOUSEBUTTONDOWN)
            # is a flip required to repair cursor move or window move????
            if self._roll_area.collidepoint(event.pos):
                break
        self.window.blits(zip(pyramids, self._roll_rects))
        self.clock.tick(40)
        pygame.display.update(self._roll_area)

    def get_start(self, roll):
        while True:
            event = self.get_next_matching_event(pygame.MOUSEBUTTONDOWN)
            if self._start_area.collidepoint(event.pos):
                return 0
            if self._board_area.collidepoint(event.pos):
                for index, rect in enumerate(self._board_squares, start=1):
                    if rect.collidepoint(event.pos):
                        return index

    def show_move(self, start, end):
        if start == 0: # move from start
            self._num_start_pieces -= 1
            self.window.blit(self.background_s,
                                      self._start_rects[self._num_start_pieces],
                                      self._start_rects[self._num_start_pieces])
        else: # move from board_square
            self.window.blit(self.background_s, self._board_squares[start-1],
                                                self._board_squares[start-1])
        if end == 15: #move to end 15 == len(board_squares) + 1 before + 1 after
            self.window.blit(self.background_s,
                                          self._end_rects[self._num_end_pieces],
                                          self._end_rects[self._num_end_pieces])
            self._num_end_pieces += 1

        # blit background over start square
        # blit piece to end square
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
