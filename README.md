# urGame
The Royal Game of Ur
In python, using pygame.
First version will allow 2p hotseat play
Then 2p play over network

Plan:
1) determine representation of board and game state.
Intended to use MVC approach to interations between UI and game model

2) Player is a more useful class than Board. So will use 2 Players to store game state information
ur_player.Player: all game state information and methods to check/execute allowable moves
ur_game: contains the controller (main) which includes game logic (time order of movesx etc)
interface: contains classes for managing Player interfaces
