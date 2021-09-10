import pygame

class PlayerInterface:

    window = None

    def __init__():

    def getMove():

    def showMove():


    pass

class LocalPlayerInterface(PlayerInterface):

    def __init__ (self, screen = None):
        super().__init__()
        if not screen:
            pygame.init()
            self._color = '
            blue'
            create stuff
        else: # self is second player - do not pygame init and use given screen
            self.screen = screen

class RemotePlayerInterface(PlayerInterface):
    pass
