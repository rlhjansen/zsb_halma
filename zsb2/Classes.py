
import class_independent_functions.py as cif




class Player:
    # number and goal are integers like:
    # 0, 1, 2, 3 these represent starting corners as in start_positions.png
    # rows stands for the amount of diagonal rows from the corner
    # size is the boardsize
    def __init__(self, number, size, rows):
        self.color = self.set_color(number)
        self.pieces = self.get_start_locations(number, size, rows)
        self.goal = self.end_loc(number, size)

    def end_location(self, number, size):
        if number == 0:
            return [size, size]
        if number == 1:
            return [0, size]
        if number == 2:
            return [size, 0]
        if number == 3:
            return [0,0]

    def get_total_manhattan(self):
        total_manhattan = 0
        for piece in self.get_pieces():
            total_manhattan += self.calculate_manhattan(piece)


    def calculate_manhattan(self, piece):
        [x,y] = piece
        manhattan = 0
        manhattan += abs(self.goal[0] - x)
        manhattan += abs(self.goal[1] - y)
        return manhattan



    def get_start_locations(self, number, size, rows):
        pieces = []
        if number == 0:
            for x in range(rows):
                for y in range(rows):
                    if x+y < rows:
                        pieces.append([x,y])
        elif number == 1:
            x_range = [size-x for x in range(rows)]
            for x in x_range:
                for y in range(rows):
                    if size-rows < x-y:
                        pieces.append([x,y])
        elif number == 2:
            y_range = [size-y for y in range(rows)]
            for x in range(rows):
                for y in y_range:
                    if size-rows < y-x:
                        pieces.append([x,y])
        elif number == 3:
            x_range = [size-x for x in range(rows)]
            y_range = [size-y for y in range(rows)]
            for x in x_range:
                for y in y_range:
                    if 2*size - rows < x+y:
                        pieces.append([x,y])
        return pieces


    def get_pieces(self):
        return self.pieces


    def set_color(self, number):
        if number == 0:
            return 'r'
        elif number == 1:
            return 'b'
        elif number == 2:
            return 'g'
        elif number == 3:
            return 'y'



class Board:
    # players = number of players
    # size is boardsize, atleast greaters than 8
    def __init__(self, players, size):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.players = [Player(player, size-1) for player in range(players)]
        self.direction_list = self.make_direction_list()
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


    def make_direction_list(self):
        dir_list = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                dir_list.append([dx, dy])
        del dir_list[4]
        return dir_list


    def make_move(self, movestring):
        [[x_start, y_start], [x_end, y_end]] = cif.to_coordinates(movestring)
        moving_player = self.board.get_player(x_start,y_start)
        moving_player.move(x_start, y_start, x_end, y_end)
        self.board[x_start][y_start] = '.'
        self.board[x_end][y_end] = moving_player


    def get_moves_player(self, player):
        moves_list = []
        for piece in player.get_pieces()
            moves_list.extend(self.get_moves_piece(piece))
        return moves_list


    def get_moves_piece(self, piece):
        moves_list_piece = []
        for [dx, dy] in self.direction_list:
            moves_list_piece.extend(self.scan(piece, dx, dy))
        return moves_list_piece

###############################################################################
    def scan(self, piece, dx, dy, only_jumps=False):
        moves_list = []
        [x, y] = piece
        new_x = x+dx
        new_y = y+dy
        while 0 <= new_x <= self.size and 0 <= new_y <= self.size:
            piece_on_coord = self.board[x][y]
            if piece_on_coord != '.':
                [jump_x, jump_y] = cif.get_jump_loc(x, y, new_x, new_y)
                if self.check_jump(x, y, new_x, new_y):
                    moves_list.append([jump_x, jump_y])
                    new_piece = [jump_x, jump_y]
                    for [new_dx, new_dy] in self.direction_list:
                        moves_list.extend(self.scan(new_piece, new_dx, new_dy, only_jumps=True))
                break
        if not only_jumps:
            if self.check_free(x+dx, y+dy):
                moves_list.append([x+dx, y+dy])
            real_moves = [[[x, y], end_loc] for end_loc in moves_list]
        else:
            real_moves = moves_list
        return real_moves



    def get_player(self, x, y):
        if self.board[x][y] == 'r':
            return self.players[0]
        elif self.board[x][y] == 'b':
            return self.players[1]
        elif self.board[x][y] == 'g':
            return self.players[2]
        elif self.board[x][y] == 'y':
            return self.players[3]


