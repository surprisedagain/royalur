import pygame
import os
from random import shuffle
from itertools import starmap
from abc import ABC, abstractmethod

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
    pygame.init()
    pygame.event.set_blocked(None) # block all events
    pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONDOWN))

    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1200, 1050)) #arg? pygame.SCALED ????

    dirname = os.path.dirname(__file__) # directory of this module's file
    background_s = pygame.image.load(os.path.join(dirname, 'images',
                                          'modern_skin', 'board.png')).convert()
    pyramid0_s = pygame.image.load(os.path.join(dirname, 'images',
                                       'modern_skin', 'pyramid0.png')).convert()
    pyramid1_s = pygame.image.load(os.path.join(dirname, 'images',
                                       'modern_skin', 'pyramid1.png')).convert()
    font = pygame.font.Font(None, 40) # default font, size 20
    cant_move_text_s = font.render('All Moves Blocked', True, pygame.Color('black'))

    window.blit(background_s, (0, 0))

    def __init__ (self, side = 'L', num_start_pieces = 7, num_end_pieces = 0):
        self._num_start_pieces = num_start_pieces
        self._num_end_pieces = num_end_pieces

        if side == 'L':
            self._piece_s = pygame.image.load(
                                  os.path.join(
                                    self.dirname, 'images', 'modern_skin', 'left_piece.png'
                                  )
                                ).convert() #???? look into alpha-convert
            self._start_rects = tuple(starmap(pygame.Rect, (
                                        ( 35, 90, 105, 105),
                                        (140, 90, 105, 105),
                                        (245, 90, 105, 105),
                                        (350, 90, 105, 105),
                                        (455, 90, 105, 105),
                                        (560, 90, 105, 105),
                                        (665, 90, 105, 105),
                                )))
            self._end_rects = tuple(starmap(pygame.Rect, (
                                        ( 35, 750, 105, 105),
                                        (140, 750, 105, 105),
                                        (245, 750, 105, 105),
                                        (350, 750, 105, 105),
                                        (455, 750, 105, 105),
                                        (560, 750, 105, 105),
                                        (665, 750, 105, 105),
                              )))
            self._board_squares = tuple(starmap(pygame.Rect, (
                                        (442, 422, 94, 94),
                                        (442, 311, 94, 94),
                                        (442, 201, 94, 94),
                                        (442,  88, 94, 94),
                                        (553,  88, 94, 94),
                                        (553, 201, 94, 94),
                                        (553, 311, 94, 94),
                                        (553, 422, 94, 94),
                                        (553, 532, 94, 94),
                                        (553, 644, 94, 94),
                                        (553, 755, 94, 94),
                                        (553, 865, 94, 94),
                                        (442, 865, 94, 94),
                                        (442, 755, 94, 94),
                                  )))
            self._roll_rects = tuple(starmap(pygame.Rect, (
                                        ( 50, 542, 100, 100),
                                        (150, 542, 100, 100),
                                        (250, 542, 100, 100),
                                        (350, 542, 100, 100),
                               )))
            self._message_rect = pygame.Rect(50, 405, 300, 150)

        else: # side == 'R' start,end,message,roll rects not correct
            self._piece_s = pygame.image.load(
                                  os.path.join(
                                    self.dirname, 'images', 'modern_skin', 'right_piece.png'
                                  )
                                ).convert() #???? look into alpha-convert
            self._start_rects = tuple(starmap(pygame.Rect, (
                                        ( 0, 260, 125, 125),
                                        (0, 260, 125, 125),
                                        (0, 260, 125, 125),
                                        (0, 260, 125, 125),
                                        (0, 260, 125, 125),
                                        (0, 260, 125, 125),
                                        (0, 260, 125, 125),
                                )))
            self._end_rects = tuple(starmap(pygame.Rect, (
                                        ( 35, 1000, 125, 125),
                                        ( 35, 1000, 125, 125),
                                        ( 35, 1000, 125, 125),
                                        ( 35, 1000, 125, 125),
                                        ( 35, 1000, 125, 125),
                                        ( 35, 1000, 125, 125),
                                        ( 35, 1000, 125, 125),

                              )))
            self._board_squares = tuple(starmap(pygame.Rect, (
                                        (737,  118, 125, 125),
                                        (737,  268, 125, 125),
                                        (737,  414, 125, 125),
                                        (737,  562, 125, 125),
                                        (737,  710, 125, 125),
                                        (737,  858, 125, 125),
                                        (737, 1006, 125, 125),
                                        (737, 1154, 125, 125),
                                        (589, 1154, 125, 125),
                                  )))

            self._roll_rects = tuple(starmap(pygame.Rect, (
                                        ( 85, 723, 100, 100),
                                        (185, 723, 100, 100),
                                        (285, 723, 100, 100),
                                        (385, 723, 100, 100),
                               )))
            self._message_rect = pygame.Rect(55, 540, 450, 150)

        self._start_area = self._start_rects[0].unionall(self._start_rects[1:])
        self._roll_area = self._roll_rects[0].unionall(self._roll_rects[1:])
        self._board_area = \
                        self._board_squares[0].unionall(self._board_squares[1:])

        # put piece images into their initial positions
        self.window.blits(((self._piece_s, rect)
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
        shuffle(pyramids)
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
        dirty_rects = []
        if start == 0: # move from start position
            self._num_start_pieces -= 1
            self.window.blit(self.background_s,
                                      self._start_rects[self._num_start_pieces],
                                      self._start_rects[self._num_start_pieces])
            dirty_rects.append(self._start_rects[self._num_start_pieces])
        else: # move from _board_square[start-1]
            self.window.blit(self.background_s, self._board_squares[start-1],
                                                self._board_squares[start-1])
            dirty_rects.append(self._board_squares[start-1])
        if end == 15: #move to end.15==len(board_squares)-1 + 1 before + 1 after
            # may need to blit from background_s if pieces misalign
            self.window.blit(self._piece_s,
                                          self._end_rects[self._num_end_pieces])
            dirty_rects.append(self._end_rects[self._num_end_pieces])
            self._num_end_pieces += 1
        else: # move to end square
            self.window.blit(self._piece_s, self._board_squares[end-1])
            dirty_rects.append(self._board_squares[end-1])
                                                
        self.clock.tick(40)
        pygame.display.update(dirty_rects)
        # end show_move

    def show_cant_move(self):
        pass


    def show_invalid_move(self, start, end):
        #pygame flash start and end rect
        pass

    def show_won(self):
        '''if not LocalPlayerInterface.result_shown:
        pygame show won message
        LocalPlayerInterface.result_shown = True'''
        pass

    def show_lost(self):
        '''if not LocalPlayerInterface.result_shown:
        pygame show lost message
        LocalPlayerInterface.result_shown = True'''
        pass

    def check_for_quit():

        if pygame.QUIT in pygame.event.get():
            raise GUIQuitException

    def close(self):
        if LocalInterface.window:
            pygame.quit()
            LocalInterface.window = None

#class RemotePlayerInterface(PlayerInterface):
#   pass
