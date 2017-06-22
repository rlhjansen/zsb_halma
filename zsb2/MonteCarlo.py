#
#
#

from __future__ import print_function
import Classes as Cl
from copy import deepcopy


def load_data(name='Database'):
    """Return a dictionary out of the database file."""
    with open(name, "r") as file:
        return eval("{" + file.read() + "}")


def reverse_move(move):
    """Return a move that negates the input move."""
    i = 1
    for char in move[1:]:
        if char.isalpha():
            break
        i += 1
    return move[i:] + move[:i]


def store(name='Database'):
    """Reset the Database file and write all contents of the dictionary."""
    with open(name, 'w') as file:
        file.truncate(0)
        for key in MCPlayer.data.keys():
            value = MCPlayer.data[key]
            file.write('"' + str(key) + '"' + ': ' + str(value) + ',\n')


class MCPlayer(Cl.Player):
    data = load_data()

    def __init__(self):
        super(MCPlayer, self).__init__()
        self.path = set()

    def board_to_key(self, board):
        """Convert the board to a key that the dictionary can use."""
        key = self.color + '\n'
        for row in board.board:
            for char in row:
                key.append(char)
            key.append('\n')
        return key

    def decide_move(self, board):
        """Return the move that will result in a board with the highest
        win rate."""
        best_score = -1
        best_move = ""
        best_board = deepcopy(board)
        for move in board.get_moves_player(self):
            board.make_move(move)
            score = self.get_win(board)

            if score and score > best_score:
                if best_move != "":
                    rev_move = reverse_move(best_move)
                    best_board.make_move(rev_move)
                    best_board.make_move(move)
                best_score = score
                best_move = move

            elif score == False:
                self.new_board(board)
                if best_score == -1:
                    best_move = move
                    best_score = 0
                    best_board.make_move(move)

            rev_move = reverse_move(move)
            board.make_move(rev_move)

        self.path.add(best_board)
        return best_move

    def new_board(self, board):
        """Make a new board setting in the dictionary."""
        key = self.board_to_key(board)
        MCPlayer.data[key] = [0, 0]

    def results(self, win):
        """Update all used board states."""
        for board in self.path:
            self.update(board, win)
        self.path = set()

    def update(self, board, win):
        """Add the results of a match to the win-percentage of a
        board setting."""
        key = self.board_to_key(board)
        value = self.data[key]
        if win:
            value[0] += 1
        value[1] += 1

    def get_win(self, board):
        """Return the win-percentage of a board setting."""
        key = self.board_to_key(board)
        value = MCPlayer.data.get(key)
        if value:
            if value[1] == 0:
                return 0
            return float(value[0]) / float(value[1])  # wins / total
        return False

