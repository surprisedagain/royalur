# written by Nathan Sinclair 10/9/21
# mood: at the overawed stage of the project too many new things

class Player(*, opponent=None):
    LENGTH = 16
    STAR_SQUARES = frozenset(4, 8, 14)

    def __init__(self):
        self._pieces = [7] + [0]*self.LENGTH-1
        self.opponent = opponent
        if opponent:
            opponent.opponent = self
        self.interface = None

    def can_move(self, roll):
        return any(self.is_valid_move(start, start+roll)
                    for start, piece in enumerate(self._pieces)
                    if piece)

    def is_valid_move(self, start, end):
        if start<0 or end>=self.LENGTH:
            return False
        if not self._pieces[start]:
            return False
        if end != 0 and end != self.LENGTH-1 and self._pieces[end]:
            return False
        if end in Board.star_squares and player._other_player._pieces[end]:
            return False
        return True

    def move(self, start, end):
        if not self._pieces[start]:
            raise ValueError('Attempted to move from empty position {start}')
        self._pieces[start] -= 1
        self._pieces[end] += 1

    def has_won(self):
        return self._pieces[-1] == 7

