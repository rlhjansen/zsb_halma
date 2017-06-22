
import imports
import class_independent_functions as cif


class Player:
    # number and goal are integers like:
    # 0, 1, 2, 3 these represent starting corners as in start_positions.png
    # rows stands for the amount of diagonal rows from the corner
    # size is the boardsize
    def __init__(self, number, size, rows):
        self.color = self.set_color(number)
        self.pieces = self.get_start_locations(number, size, rows)
        self.goal = self.goal_location(number, size)
        self.goal_manhattan = self.calc_goal_manhattan(rows)

    # checks
    def calc_goal_manhattan(self, rows):
        goal_manhattan = 0
        for i in range(rows):
            for _ in range(i+1):
                goal_manhattan += i
        return goal_manhattan

    # checks if the player wins
    def player_wins(self):
        if self.get_total_manhattan() == self.goal_manhattan:
            return True
        else:
            return False


    # returns a player's goal location, the opposite side of the board
    def goal_location(self, number, size):
        if number == 0:
            return [size, size]
        if number == 2:
            return [0, size]
        if number == 3:
            return [size, 0]
        if number == 1:
            return [0, 0]

    # returns the sum of all manhattan distances of a players pieces to his
    # goal location - the opposite corner -
    def get_total_manhattan(self):
        total_manhattan = 0
        for piece in self.get_pieces():
            total_manhattan += self.calculate_manhattan(piece)
        return total_manhattan


    # returns the manhattan distance from a piece to the goal location
    # of that player - the opposite corner -
    def calculate_manhattan(self, piece):
        [x,y] = piece
        manhattan = 0
        manhattan += abs(self.goal[0] - x)
        manhattan += abs(self.goal[1] - y)
        return manhattan

    # moves the piece in the player's piecelist
    def move_piece(self, x_start, y_start, x_end, y_end):
        for i in range(len(self.pieces)):
            [x, y] = self.pieces[i]
            if x == x_start and y == y_start:
                self.pieces[i] = [x_end, y_end]
            break

    # returns starting locations for a player
    def get_start_locations(self, number, size, rows):
        pieces = []
        if number == 0:
            for x in range(rows):
                for y in range(rows):
                    if x+y < rows:
                        pieces.append([x,y])
        elif number == 2:
            x_range = [size-x for x in range(rows)]
            for x in x_range:
                for y in range(rows):
                    if size-rows < x-y:
                        pieces.append([x,y])
        elif number == 3:
            y_range = [size-y for y in range(rows)]
            for x in range(rows):
                for y in y_range:
                    if size-rows < y-x:
                        pieces.append([x,y])
        elif number == 1:
            x_range = [size-x for x in range(rows)]
            y_range = [size-y for y in range(rows)]
            for x in x_range:
                for y in y_range:
                    if 2*size - rows < x+y:
                        pieces.append([x,y])
        return pieces

    # returns the current piece locations for a player
    def get_pieces(self):
        return self.pieces

    # assigns a color to the player
    def set_color(self, number):
        if number == 0:
            return 'r'
        elif number == 1:
            return 'b'
        elif number == 2:
            return 'g'
        elif number == 3:
            return 'y'

    # returns the color of a player
    def get_color(self):
        return self.color

    # enter move from console, i.e. a3a4, or a3a5a7 when jumping
    # enter q to quit
    def decide_move(self, board):
        chosen_move = raw_input('enter a move:')
        if chosen_move == 'q':
            exit(0)
        return chosen_move

    def player_whole_colour(self):
        if self.color == 'r':
            return 'Red'
        elif self.color == 'b':
            return 'Blue'
        elif self.color == 'g':
            return 'Green'
        elif self.color == 'y':
            return 'Yellow'

    def results(self, Boolean):
        pass

class Board:
    # players = number of players
    # size is boardsize, atleast greaters than 8
    # rows = diagonal rows of pawns
    # playertypes = list of playertipes i.e. ['h'
    def __init__(self, players, size, rows, playertypes):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.players = [Player(player, size-1, rows) for player in range(players)]
        self.size = size - 1
        self.direction_list = self.make_direction_list()
        self.color_player_dict = self.make_player_dictionary(players)
        for player in self.players:
            for [x,y] in player.get_pieces():
                self.board[x][y] = player.get_color()
        self.current_turn = self.players[0]

    def init_players(self, players, size, rows):
        self.players = []
        for i in range(len(players)):
            if players[i] == 'h':
                self.players.append(Player(i, size - 1, rows))
            #elif players[i] == 'mc':
            #    self.players.append(MCPlayer(i, size - 1, rows))
            #elif players[i] == 'ab':
            #    self.players.append(AlfaBetaPlayer(i, size - 1, rows))

    # returns the score for a player for the current board
    # 200 here is supposed to drive the player to a win.
    def get_score(self, player):
        score = 0
        score += self.players[player].get_total_manhattan()
        if self.players[player].player_wins():
            score -= 200
        for other_player in self.players:
            if self.players[player] != other_player:
                score -= other_player.get_total_manhattan()
                if other_player.player_wins():
                    score += 200
        return score

    # set self.current_turn to next player
    def next_player(self):
        for i in range(len(self.players)):
            if self.players[i] == self.current_turn and i != len(self.players) - 1:
                self.current_turn = self.players[i+1]
                break
            else:
                self.current_turn = self.players[0]


    # returns a dictionary that returns a player object, with color input
    def make_player_dictionary(self, number_of_players):
        colorlist = ['r', 'b', 'g', 'y']
        player_dict = {}
        for i in range(number_of_players):
            player_dict[colorlist[i]] = self.players[i]
        return player_dict

    # returns a list with x,y direction combinations that are allowed to explore
    # in
    def make_direction_list(self):
        dir_list = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                dir_list.append([dx, dy])
        del dir_list[4]
        return dir_list

    # make an actual move on the board
    def make_move(self, movestring):
        [[x_start, y_start], [x_end, y_end]] = cif.to_coordinates(movestring, self.size)
        objectstring = self.board[x_start][y_start]
        moving_player = self.player_string_to_player(objectstring)
        self.board[x_start][y_start] = '.'
        self.board[x_end][y_end] = objectstring
        self.make_move_for_player(moving_player, x_start, y_start, x_end, y_end)
        self.next_player()

    # makes sure that the player.pieces are congruent with the pieces on the board
    def make_move_for_player(self, moving_player, x_start, y_start, x_end, y_end):
        moving_player.move_piece(x_start, y_start, x_end, y_end)


    # returns a player object for a string input color
    def player_string_to_player(self, string):
        return self.color_player_dict[string]


    # returns a list of legal moves that a player can make
    def get_moves_player(self, player):
        moves_list = []
        if type(player) == int:
            for piece in self.players[player-1].get_pieces():
                moves_list.extend(self.get_moves_piece(piece))
        else:
            for piece in player.get_pieces():
                moves_list.extend(self.get_moves_piece(piece))
        return moves_list

    # returns a list of moves that a piece can make
    def get_moves_piece(self, piece):
        moves_list_piece = []
        for [dx, dy] in self.direction_list:
            moves_list_piece.extend(self.scan(piece, dx, dy))
        return moves_list_piece

    # returns a list of possible moves when exploring a certain direction
    # only_jumps=True is used when there is a gamepiece in the explored
    # direction that can be jumped over, in that case all possible further jumps
    # are evaluated, return format = [[start_x, start_y], [end_x, end_y]]
    def scan(self, piece, dx, dy, only_jumps=False):
        moves_list = []
        [x, y] = piece
        new_x = x+dx
        new_y = y+dy
        while 0 <= new_x <= self.size and 0 <= new_y <= self.size:
            piece_on_coord = self.board[x][y]
            if piece_on_coord != '.':
                [jump_x, jump_y] = cif.get_jump_loc(x, y, new_x, new_y)
                if self.on_board(jump_x, jump_y):
                    if self.check_jump(new_x, new_y, jump_x, jump_y, dx, dy) and \
                        self.check_free(jump_x, jump_y):
                        moves_list.append([jump_x, jump_y])
                        new_piece = [jump_x, jump_y]
                        for [new_dx, new_dy] in self.direction_list:
                            temp_move = self.scan(new_piece, new_dx, new_dy, only_jumps=True)
                            if temp_move != []:
                                moves_list.append(self.scan(new_piece, new_dx, new_dy, only_jumps=True))
                break
            new_x += dx
            new_y += dy
        if not only_jumps:
            if self.on_board(x+dx, y+dy):
                if self.check_free(x+dx, y+dy):
                    moves_list.append([x+dx, y+dy])
            real_moves = [[[x, y], end_loc] for end_loc in moves_list]
        else:
            real_moves = moves_list
        return real_moves

    # checks if there's a piece on the start position mentioned
    # checks if the move is in the list of that players possible moves
    def check_not_legal(self, move):
        movelist = cif.to_coordinates(move, self.size)
        x, y = movelist[0][0], movelist[0][1]
        if self.board[x][y] == '.':
            print("there is no piece on that position")
            return True
        else:
            player = self.color_player_dict[self.board[x][y]]
            if player == self.current_turn:
                if movelist in self.get_moves_piece([x,y]):
                    if player == self.current_turn:
                        return False
                else:
                    return True
                    print("that's not a valid move")
            else:
                print("you're not that player")
                return True


    # checks if a position on the board is unoccupied
    def check_free(self, x, y):
        if self.board[x][y] == '.':
            return True
        else:
            return False

    # checks if a position can be jumped toward, with encountering blocking
    # pieces
    def check_jump(self, x, y, land_x, land_y, dx, dy):
        new_x = x
        new_y = y
        while new_x != land_x and new_y != land_y:
            new_x = x+dx
            new_y = y+dy
            if self.board[new_x][new_y] != '.':
                return False
        return True

    # return the corresponding player of a piece on position x,y
    def get_player(self, x, y):
        return self.color_player_dict[self.board[x][y]]

    # prints the current board
    def print_board(self):
        for row in self.board:
            print(row)

    # returns a copy of the board
    def get_board(self):
        new_board = self
        return new_board

    # checks if a position [x,y] is on the board
    def on_board(self, x, y):
        if 0 <= x <= self.size and 0 <= y <= self.size:
            return True
        else:
            return False


    def no_winner_yet(self):
        no_winner = True
        for player in self.players:
            if player.player_wins():
                no_winner = False
        return no_winner

    def who_won(self):
        for player in self.players:
            if player.player_wins():
                return player.player_whole_colour()





def main_game_loop(halma_board):
    turn = 1
    while halma_board.no_winner_yet():
        print("turn", turn)
        halma_board.print_board()
        not_legal = True
        while not_legal:
            move = halma_board.current_turn.decide_move(halma_board)
            if move == 'check moves':
                print([x for x in cif.to_movestrings(halma_board.get_moves_player(halma_board.current_turn), halma_board.size)])
            elif move == 'manhattan':
                print(halma_board.current_turn.get_total_manhattan())
            elif move == 'goalmanhattan':
                print(halma_board.current_turn.goal_manhattan)
            else:
                not_legal = halma_board.check_not_legal(move)
        #drawfile.draw(halma_board, move)
        halma_board.make_move(move)
        turn += 1
    for player in halma_board.players:
        player.results(player.player_wins())
    winner = halma_board.who_won()
    print("Congratulations!, the ", winner, "has won!")


def ask_new_game():
    new_game = raw_input("Do you want to start a new game? (y/n):")
    while True:
        if new_game == 'y':
            return True
        elif new_game == 'n':
            return False
        else:
            print("that's not a valid option")
            new_game = raw_input("Do you want to start a new game? (y/n):")

halma_board = Board(2, 2, 1, ['h', 'c'])
main_game_loop(halma_board)