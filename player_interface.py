import pygame
from abc import ABC

class PlayerInterface(ABC):

    @abstractmethod
    def get_roll():
        pass

    @abstractmethod
    def get_move(roll):
        pass

    @abstractmethod
    def show_move(start, end):
        pass

    @abstractmethod
    def show_result(winner):
        pass

class LocalPlayerInterface(PlayerInterface):
    display = None

    def __init__ (self):
        super().__init__()
        if not LocalPlayerInterface.display:
            pygame.init()
            self._color = '
            blue'
            create stuff
        else: # self is second player - do not pygame init and use given screen
            self.screen = screen

class RemotePlayerInterface(PlayerInterface):
    pass
