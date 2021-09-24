# written by Nathan Sinclair 10/9/21
# mood: at the overawed stage of the project too many new things

from random import randrange

class Player():
    LENGTH = 16
    FIRST_COMBAT = 5
    FIRST_SAFE_AGAIN = 13
    COMBAT_STAR = 8
    STARS = frozenset((4, 8, 14))

    def __init__(self, interface, *, opponent=None):
        self._pieces = [7] + [0]*(self.LENGTH-1)
        self.opponent = opponent
        if opponent:
            opponent.opponent = self
        self.interface = interface

    def can_move(self, roll):
        if roll == 0:
            return False
        return any(self.is_valid_move(start, start+roll)
                    for start, piece in enumerate(self._pieces)
                    if piece)

    def is_valid_move(self, start, end):
        if not 0 <= start < end < self.LENGTH:
            return False
        if not self._pieces[start]:
            return False
        if end != 0 and end != self.LENGTH-1 and self._pieces[end]:
            return False
        if end == self.COMBAT_STAR and self.opponent._pieces[self.COMBAT_STAR]:
            return False
        return True

    @staticmethod
    def roll_pyramids():
        return sum(randrange(2) for _ in range(4))

    def move(self, start, end):
        if not self._pieces[start]:
            raise ValueError(f'Attempted to move from empty position {start}')
        take = False
        if self.FIRST_COMBAT <= end < self.FIRST_SAFE_AGAIN and self.opponent._pieces[end]:
            take = True
            self.opponent._pieces[end] -= 1
            self.opponent._pieces[0] += 1
        self._pieces[start] -= 1
        self._pieces[end] += 1
        return (end in self.STARS, take)

    def has_won(self):
        return self._pieces[-1] == 7

if __name__ == '__main__':
    player1 = Player()
    player2 = Player(opponent = player1)
    print(f'Expect True:: {player1.can_move(3)=}')
    print(f'Expect False:: {player1.move(0, 3)=}')
    print(f'Expect True:: {player1.move(3, 4)=}')
    print(f'Expect [6,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]:: {player1._pieces=}')
    print(f'Expect True:: {player1.can_move(4)=}')
    print(f'Expect False:: {player1.is_valid_move(0, 4)=}')
    print(f'Expect False:: {player1.move(0, 2)=}')
    print(f'Expect False:: {player1.move(0, 6)=}')
    print(f'Expect True:: {player2.move(0, 8)=}')
    print(f'Expect False:: {player1.can_move(2)=}')
    print(f'Expect False:: {player2.move(8, 10)=}')
    print(f'Expect True:: {player1.can_move(2)=}')
    print(f'Expect False:: {player1.move(6, 10)=}')
    print(f'Expect [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:: {player2._pieces=}')
