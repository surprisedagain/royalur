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
    MAX_WIDTH, MAX_HEIGHT = 1200, 1050
    pygame.init()
    pygame.event.set_blocked(None) # block all events
    pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONDOWN))

    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    ratio = min(screen_width/MAX_WIDTH, screen_height/MAX_HEIGHT, 1)


    clock = pygame.time.Clock()
    window = pygame.display.set_mode((int(ratio*MAX_WIDTH),
                                                         int(ratio*MAX_HEIGHT)))

    dirname = os.path.dirname(__file__) # directory of this module's file
    background_s = scale_surface(pygame.image.load(os.path.join(
               dirname, 'images', 'modern_skin', 'board.png')).convert(), ratio)
    pyramid0_s = scale_surface(pygame.image.load(os.path.join(
            dirname, 'images', 'modern_skin', 'pyramid0.png')).convert(), ratio)
    pyramid1_s = scale_surface(pygame.image.load(os.path.join(
            dirname, 'images', 'modern_skin', 'pyramid1.png')).convert(), ratio)

    #font = pygame.font.Font(None, 40) # default font, size 20
    #cant_move_text_s = font.render('All Moves Blocked', True,
                                                          #pygame.Color('black'))
    window.blit(background_s, (0, 0))

    def __init__ (self, side = 'L', num_start_pieces = 7, num_end_pieces = 0):
        self._num_start_pieces = num_start_pieces
        self._num_end_pieces = num_end_pieces

        if side == 'L':
            self._piece_s = scale_surface(pygame.image.load(
                                   os.path.join(
                                     self.dirname, 'images', 'modern_skin',
                                       'blue_piece.png'
                                   )
                                ).convert_alpha(), self.ratio)
            self._piece_small_s = scale_surface(pygame.image.load(
                                    os.path.join(
                                     self.dirname, 'images', 'modern_skin',
                                       'blue_small_piece.png'
                                    )
                                ).convert_alpha(), self.ratio)
            self._start_rects = tuple(map(
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
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
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
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
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
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
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
                                      (
                                        ( 15, 542, 100, 100),
                                        (115, 542, 100, 100),
                                        (215, 542, 100, 100),
                                        (315, 542, 100, 100),
                               )))
            self._message_rect = pygame.Rect(scale_tuple((50, 405, 300, 150), self.ratio))

        else: # side == 'R' start,end,message,roll rects not correct
            self._piece_s = scale_surface(pygame.image.load(
                                   os.path.join(
                                     self.dirname, 'images', 'modern_skin',
                                     'red_piece.png'
                                   )
                                ).convert_alpha(), self.ratio)
            self._piece_small_s = scale_surface(pygame.image.load(
                                    os.path.join(
                                      self.dirname, 'images', 'modern_skin',
                                      'red_small_piece.png'
                                    )
                                ).convert_alpha(), self.ratio)
            self._start_rects = tuple(map(
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
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
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
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
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
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
                              lambda t: pygame.Rect(scale_tuple(t, self.ratio)), 
                                      (
                                        ( 785, 542, 100, 100),
                                        ( 885, 542, 100, 100),
                                        ( 985, 542, 100, 100),
                                        (1085, 542, 100, 100),
                               )))
            self._message_rect = pygame.Rect(scale_tuple(
                                               (55, 540, 450, 150), self.ratio))

        self._start_area = self._start_rects[0].unionall(self._start_rects[1:])
        self._roll_area = self._roll_rects[0].unionall(self._roll_rects[1:])
        self._board_area = \
                        self._board_squares[0].unionall(self._board_squares[1:])

        # put piece images into their initial positions
        self.window.blits(((self._piece_small_s, rect)
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
            self.window.blit(self._piece_small_s,
                                          self._end_rects[self._num_end_pieces])
            dirty_rects.append(self._end_rects[self._num_end_pieces])
            self._num_end_pieces += 1
        else: # move to end square
            self.window.blit(self._piece_s, self._board_squares[end-1])
            dirty_rects.append(self._board_squares[end-1])
                                                
        self.clock.tick(40)
        pygame.display.update(dirty_rects)
        # end show_move

    def show_taken(self): # this may be bodgy - better to have a complete show opponents move
        self.window.blit(self._piece_small_s,
                                      self._start_rects[self._num_start_pieces])
        self.clock.tick(40)
        pygame.display.update(self._start_rects[self._num_start_pieces])
        self._num_start_pieces += 1

    def show_cant_move(self, roll):
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

    def check_for_quit(self):
        if pygame.QUIT in pygame.event.get():
            raise GUIQuitException

    def close(self):
        if LocalInterface.window:
            pygame.quit()
            LocalInterface.window = None

#class RemotePlayerInterface(PlayerInterface):
#   pass
