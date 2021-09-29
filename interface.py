import pygame
import os
from random import shuffle
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

def scale_surface(surface, ratio):
    if ratio == 1:
        return surface
    #else:
    return pygame.transform.smoothscale(surface,
                                       scale_tuple(surface.get_size(), ratio))

def scale_tuple(tuple_, ratio):
    if ratio == 1:
        return tuple_
    #else:
    return tuple(int(ratio*num) for num in tuple_)

class LocalInterface(PlayerInterface):
    pygame.init()
    pygame.event.set_blocked(None) # block all events
    pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONDOWN))

    info = pygame.display.Info()
    MAX_WIDTH, MAX_HEIGHT = 1200, 1050
    screen_width, screen_height = info.current_w, info.current_h
    _ratio = min((screen_width-100)/MAX_WIDTH, (screen_height-100)/MAX_HEIGHT, 1)


    pygame.display.set_caption('Ur')
    _clock = pygame.time.Clock()
    _window = pygame.display.set_mode((int(_ratio*MAX_WIDTH),
                                                        int(_ratio*MAX_HEIGHT)))

    dirname = os.path.dirname(__file__) # directory of this module's file
    _background_s = scale_surface(pygame.image.load(os.path.join(
              dirname, 'images', 'modern_skin', 'board.png')).convert(), _ratio)
    _pyramid0_s = scale_surface(pygame.image.load(os.path.join(
           dirname, 'images', 'modern_skin', 'pyramid0.png')).convert(), _ratio)
    _pyramid1_s = scale_surface(pygame.image.load(os.path.join(
           dirname, 'images', 'modern_skin', 'pyramid1.png')).convert(), _ratio)

    _roll_msg_s = scale_surface(pygame.image.load(os.path.join(dirname,
              'images', 'modern_skin', 'roll.png')).convert(), _ratio)
    _roll_bold_msg_s = scale_surface(pygame.image.load(os.path.join(dirname,
              'images', 'modern_skin', 'roll_bold.png')).convert(), _ratio)
    _move_msg_s = [
            scale_surface(pygame.image.load(os.path.join(dirname,
                      'images', 'modern_skin', 'move0.png')).convert(), _ratio),
            scale_surface(pygame.image.load(os.path.join(dirname,
                      'images', 'modern_skin', 'move1.png')).convert(), _ratio),
            scale_surface(pygame.image.load(os.path.join(dirname,
                      'images', 'modern_skin', 'move2.png')).convert(), _ratio),
            scale_surface(pygame.image.load(os.path.join(dirname,
                      'images', 'modern_skin', 'move3.png')).convert(), _ratio),
            scale_surface(pygame.image.load(os.path.join(dirname,
                      'images', 'modern_skin', 'move4.png')).convert(), _ratio)
    ]
    _victory_msg_s = scale_surface(pygame.image.load(os.path.join(dirname,
                     'images', 'modern_skin', 'victory.png')).convert(), _ratio)

    _window.blit(_background_s, (0, 0))

    def __init__ (self, side = 'L', num_start_pieces = 7, num_end_pieces = 0):
        self._num_start_pieces = num_start_pieces
        self._num_end_pieces = num_end_pieces

        if side == 'L':
            self._piece_s = scale_surface(pygame.image.load(
                                   os.path.join(
                                     self.dirname, 'images', 'modern_skin',
                                       'blue_piece.png'
                                   )
                                ).convert_alpha(), self._ratio)
            self._piece_small_s = scale_surface(pygame.image.load(
                                    os.path.join(
                                     self.dirname, 'images', 'modern_skin',
                                       'blue_small_piece.png'
                                    )
                                ).convert_alpha(), self._ratio)
            self._start_rects = tuple(map(
                             lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        ( 30, 90, 50, 50),
                                        ( 85, 90, 50, 50),
                                        (140, 90, 50, 50),
                                        (195, 90, 50, 50),
                                        (250, 90, 50, 50),
                                        (305, 90, 50, 50),
                                        (360, 90, 50, 50),
                                )))
            self._end_rects = tuple(map(
                             lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        ( 30, 750, 50, 50),
                                        ( 85, 750, 50, 50),
                                        (140, 750, 50, 50),
                                        (195, 750, 50, 50),
                                        (250, 750, 50, 50),
                                        (305, 750, 50, 50),
                                        (360, 750, 50, 50),
                              )))
            self._board_squares = tuple(map(
                             lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        (443, 422, 94, 94),
                                        (443, 310, 94, 94),
                                        (443, 200, 94, 94),
                                        (443,  88, 94, 94),
                                        (554,  88, 94, 94),
                                        (554, 200, 94, 94),
                                        (554, 310, 94, 94),
                                        (554, 422, 94, 94),
                                        (554, 532, 94, 94),
                                        (554, 644, 94, 94),
                                        (554, 755, 94, 94),
                                        (554, 865, 94, 94),
                                        (443, 865, 94, 94),
                                        (443, 755, 94, 94),
                                  )))
            self._roll_rects = tuple(map(
                             lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        ( 15, 542, 101, 101),
                                        (115, 542, 101, 101),
                                        (215, 542, 101, 101),
                                        (315, 542, 101, 101),
                               )))
            self._msg_rect = pygame.Rect(scale_tuple((6, 390, 418, 130),
                                                                   self._ratio))

        else: # side == 'R' start,end,message,roll rects not correct
            self._piece_s = scale_surface(pygame.image.load(
                                   os.path.join(
                                     self.dirname, 'images', 'modern_skin',
                                     'red_piece.png'
                                   )
                                ).convert_alpha(), self._ratio)
            self._piece_small_s = scale_surface(pygame.image.load(
                                    os.path.join(
                                      self.dirname, 'images', 'modern_skin',
                                      'red_small_piece.png'
                                    )
                                ).convert_alpha(), self._ratio)
            self._start_rects = tuple(map(
                              lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        ( 790, 90, 55, 55),
                                        ( 845, 90, 55, 55),
                                        ( 900, 90, 55, 55),
                                        ( 955, 90, 55, 55),
                                        (1010, 90, 55, 55),
                                        (1065, 90, 55, 55),
                                        (1120, 90, 55, 55),
                                )))
            self._end_rects = tuple(map(
                              lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        ( 790, 750, 55, 55),
                                        ( 845, 750, 55, 55),
                                        ( 900, 750, 55, 55),
                                        ( 955, 750, 55, 55),
                                        (1010, 750, 55, 55),
                                        (1065, 750, 55, 55),
                                        (1120, 750, 55, 55),
                              )))
            self._board_squares = tuple(map(
                             lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        (663, 422, 94, 94),
                                        (663, 310, 94, 94),
                                        (663, 200, 94, 94),
                                        (663,  88, 94, 94),
                                        (554,  88, 94, 94),
                                        (554, 200, 94, 94),
                                        (554, 310, 94, 94),
                                        (554, 422, 94, 94),
                                        (554, 532, 94, 94),
                                        (554, 644, 94, 94),
                                        (554, 755, 94, 94),
                                        (554, 865, 94, 94),
                                        (663, 865, 94, 94),
                                        (663, 755, 94, 94),
                                  )))
            self._roll_rects = tuple(map(
                              lambda t: pygame.Rect(scale_tuple(t, self._ratio)), 
                                      (
                                        ( 785, 542, 101, 101),
                                        ( 885, 542, 101, 101),
                                        ( 985, 542, 101, 101),
                                        (1085, 542, 101, 101),
                               )))
            self._msg_rect = pygame.Rect(scale_tuple((776, 390, 418, 130),
                                                                   self._ratio))

        self._start_area = self._start_rects[0].unionall(self._start_rects[1:])
        self._roll_area = self._msg_rect.unionall(self._roll_rects)
        self._board_area = \
                        self._board_squares[0].unionall(self._board_squares[1:])

        # put piece images into their initial positions
        self._window.blits(((self._piece_small_s, rect)
                    for rect in self._start_rects[:self._num_start_pieces]))
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
        pyramids = [self._pyramid1_s] * roll + [self._pyramid0_s] * (4 - roll)
        shuffle(pyramids)

        self._window.blit(self._roll_msg_s, self._msg_rect)
        pygame.display.update(self._msg_rect)

        pygame.event.set_allowed(pygame.MOUSEMOTION)
        roll_msg_isbold = False
        while True: # wait until BUTTONDOWN in _roll_area
            event = self.get_next_matching_event(pygame.MOUSEBUTTONDOWN,
                                                             pygame.MOUSEMOTION)
            if self._roll_area.collidepoint(event.pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    break
                if event.type == pygame.MOUSEMOTION and not roll_msg_isbold:
                    roll_msg_isbold = True
                    self._window.blit(self._roll_bold_msg_s, self._msg_rect)
            elif roll_msg_isbold:
                roll_msg_isbold = False
                self._window.blit(self._roll_msg_s, self._msg_rect)
            self._clock.tick(40)
            pygame.display.update(self._msg_rect)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self._window.blits(zip(pyramids, self._roll_rects))
        pygame.display.update(self._roll_area)


    def get_start(self, roll):
        self._window.blit(self._move_msg_s[roll], self._msg_rect)
        pygame.display.update(self._roll_area)
        result = None
        while result == None:
            event = self.get_next_matching_event(pygame.MOUSEBUTTONDOWN)
            if self._start_area.collidepoint(event.pos):
                result = 0
            if self._board_area.collidepoint(event.pos):
                for index, rect in enumerate(self._board_squares, start=1):
                    if rect.collidepoint(event.pos):
                        result = index
        self._window.blit(self._background_s, self._msg_rect, self._msg_rect)
        pygame.display.update(self._roll_area)
        return result


    def show_move(self, start, end):
        dirty_rects = []
        if start == 0: # move from start position
            self._num_start_pieces -= 1
            self._window.blit(self._background_s,
                                      self._start_rects[self._num_start_pieces],
                                      self._start_rects[self._num_start_pieces])
            dirty_rects.append(self._start_rects[self._num_start_pieces])
        else: # move from _board_square[start-1]
            self._window.blit(self._background_s, self._board_squares[start-1],
                                                self._board_squares[start-1])
            dirty_rects.append(self._board_squares[start-1])
        if end == 15: #move to end 15==len(board_squares)-1 + 1 before + 1 after
            self._window.blit(self._piece_small_s,
                                          self._end_rects[self._num_end_pieces])
            dirty_rects.append(self._end_rects[self._num_end_pieces])
            self._num_end_pieces += 1
        else: # move to end square
            self._window.blit(self._background_s, self._board_squares[end-1],
                                                     self._board_squares[end-1])
            self._window.blit(self._piece_s, self._board_squares[end-1])
            dirty_rects.append(self._board_squares[end-1])
                                                
        self._clock.tick(40) #if this line ommitted victory message not show
        pygame.display.update(dirty_rects)
        # end show_move

    def show_taken(self): # this may be bodgy - better to have a complete show opponents move
        self._window.blit(self._piece_small_s,
                                      self._start_rects[self._num_start_pieces])
        self._clock.tick(40) #if this line omitted display lags
        pygame.display.update(self._start_rects[self._num_start_pieces])
        self._num_start_pieces += 1

    def show_cant_move(self, roll):
        self._window.blit(self._move_msg_s[0], self._msg_rect)
        pygame.display.update(self._msg_rect)
        pygame.time.wait(1500)
        self._window.blit(self._background_s, self._msg_rect, self._msg_rect)
        pygame.display.update(self._msg_rect)


    def show_invalid_move(self, start, end):
        #pygame flash start and end rect
        pass

    def show_won(self):
        self._clock.tick(40)
        self._window.blit(self._victory_msg_s, self._msg_rect)
        pygame.display.update(self._msg_rect)

    def show_lost(self):
        pass

    def check_for_quit(self):
        self._clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise GUIQuitException

    def close(self):
        if LocalInterface._window:
            pygame.quit()
            LocalInterface._window = None

#class RemotePlayerInterface(PlayerInterface):
#   pass
