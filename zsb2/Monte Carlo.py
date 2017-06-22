#
#
#

import Classes as Cl


class MCPlayer(Cl.Player):

    def __init__(self):
        super(MCPlayer, self).__init__()
        self.data = {}
        self.load_data()

    def decide_move(self, board):
        return self.find_best_move(board)

    # finding the best move from the current situation
    def find_best_move(self, board):
        best_score = -1
        best_move = ""
        for move in board.get_moves_player(self):
            new_board = board.make_move(move)
            new_board.check_board_exist()
            score = self.data[new_board]
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def load_data(self, name='Database'):
        with open(name, "r") as file:
            self.data = eval("{" + file.read() + "}")

    def save(self, key, value, name='Database'):
        self.data[key] = value
        with open(name, "a") as file:
            file.write('"' + str(key) + '"' + ': ' + str(value) + ',\n')


database = load_data()
save(database, 'key', '\"value\"')
print(database['key'])
