class Board:
    # players = number of players
    # size is boardsize, atleast greaters than 8
    def __init__(self, players, size):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.players = [Player(player, size) for player in range(players)]
        for player in self.players:
            for [x,y] in player.get_piece_coords():
                self.board[x][y] = player.get_color()

    def get_score(self, player):
        score = 0
        score += player.get_total_manhattan()
        for other_player in self.players:
            if player != other_player:
                score -= other_player.get_total_manhattan()
        return score


    def make_move(self, movestring):
        [[x_start, y_start], [x_end, y_end]] = to_coordinates(movestring)
        moving_player = self.board.get_player(x_start,y_start)
        moving_player.move()
        self.board[x_start][y_start] = '.'
        self.board[x_end][y_end] = moving_player

    def get_player(self, x, y):
        return self.board[x][y]








