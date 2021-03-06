# Classes.py
# by Artemis ??? (00000000), Jesper ??? (00000000), Jochem Holscher (11007729),
# Marijn ??? (00000000) and Reitze Jansen (00000000).
# ------------------------------------------------------------------------------
# This program runs a halma board. 3 types of players can play on this board:
# 1. Humans, they will be asked for input moves.
# 2. Monte Carlo, it will give input based on a database.
# 3. Alpha Beta, it will give input based on the alpha-beta algorithm.

from __future__ import print_function
import class_independent_functions as cif
from random import randint
from copy import deepcopy
from time import time, sleep
from visual import *


class Player:
    # number and goal are integers like:
    # 0, 1, 2, 3 these represent starting corners as in start_positions.png
    # rows stands for the amount of diagonal rows from the corner
    # size is the boardsize
    def __init__(self, number, size, rows, type):
        self.type = type
        self.color = self.set_color(number)
        self.number = number
        self.size = size
        self.rows = rows
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
    # human player
    def decide_move(self, board):
        chosen_move = ""
        while True:
            chosen_move = raw_input('enter a move:')
            if chosen_move != "":
                break
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
        return 0


class Board:
    # players = number of players
    # size is boardsize, atleast greaters than 8
    # rows = diagonal rows of pawns
    # playertypes = list of playertipes i.e. ['h'
    def __init__(self, players, size, rows, playertypes):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.players = self.init_players(playertypes, size, rows)
        self.size = size - 1
        self.direction_list = self.make_direction_list()
        self.color_player_dict = self.make_player_dictionary(players)
        for player in self.players:
            for [x,y] in player.get_pieces():
                self.board[x][y] = player.get_color()
        self.current_turn = self.players[0]
        self.test_run = self.only_mc_players()

    def init_players(self, players, size, rows):
        player_list = []
        for i in range(len(players)):
            if players[i] == 'h':
                player_list.append(Player(i, size - 1, rows, 'h'))
            elif players[i] == 'mc':
                player_list.append(MCPlayer(i, size - 1, rows, 'mc'))
            elif players[i] == 'ab':
                player_list.append(ABPlayer(i, size - 1, rows, 'ab'))
        return player_list

    def only_mc_players(self):
        for player in self.players:
            if player.type != 'mc':
                return False
        return True

    def reset_board(self):
        for pl in self.players:
            pl.pieces = pl.get_start_locations(pl.number, pl.size, pl.rows)
        self.board = [['.' for _ in range(self.size + 1)] for _ in range(self.size+1)]
        for player in self.players:
            for [x,y] in player.get_pieces():
                self.board[x][y] = player.get_color()
        self.current_turn = self.players[0]

    # returns the value of the board. Red favours a higher score, blue a lower.
    def get_score(self):
        red = self.players[0]
        blue = self.players[1]
        score = -red.get_total_manhattan()
        score += blue.get_total_manhattan()
        return score

    # set self.current_turn to next player
    def next_player(self):
        for i in range(len(self.players)):
            if self.players[i] == self.current_turn and i != len(self.players) - 1:
                self.current_turn = self.players[i+1]
                break
            else:
                self.current_turn = self.players[0]

    # Return the player that will have the turn after the given player.
    def get_next_player(self, player):
        index = self.players.index(player) + 1

        if index == len(self.players):
            return self.players[0]
        return self.players[index]

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
        start_x, start_y = piece
        for [dx, dy] in self.direction_list:
            moves_list_piece.extend(self.scan(start_x, start_y, dx, dy, set()))
        return moves_list_piece

    # returns a list of possible moves when exploring a certain direction
    # only_jumps=True is used when there is a gamepiece in the explored
    # direction that can be jumped over, in that case all possible further jumps
    # are evaluated, return format = [[start_x, start_y], [end_x, end_y]]
    def scan(self, start_x, start_y, dx, dy, visited, both=True):
        try_x = start_x+dx
        try_y = start_y+dy
        moves = []
        jumps = set()
        visited_set = set()
        for x in visited:
            visited_set.add(x)
        if self.on_board(try_x,try_y):
            if self.check_free(try_x, try_y):
                moves.append([(start_x, start_y), (try_x, try_y)])
        new_x = start_x+dx
        new_y = start_y+dy
        jump_x, jump_y = cif.get_jump_loc(start_x,start_y,new_x,new_y)
        while self.on_board(jump_x, jump_y):
            if (jump_x, jump_y) not in visited_set:
                if self.check_free(jump_x, jump_y):
                    middle_x = (jump_x+start_x)/2
                    middle_y = (jump_y+start_y)/2
                    if self.board[middle_x][middle_y] != '.':
                        if self.check_inbetween(start_x, start_y, middle_x, middle_y, jump_x, jump_y, dx, dy):
                            jumps.add((jump_x, jump_y))
                            visited_set.add((start_x, start_y))
                            if both:
                                colour = self.board[start_x][start_y]
                                self.board[start_x][start_y] = '.'
                            for newdx, newdy in self.direction_list:
                                jumps |= self.scan(jump_x, jump_y, newdx, newdy, visited_set, both=False)
                            if both:
                                self.board[start_x][start_y] = colour
            else:
                break
            new_x += dx
            new_y += dy
            jump_x, jump_y = cif.get_jump_loc(start_x, start_y, new_x, new_y)
        if both:
            for jump in jumps:
                moves.append([(start_x,start_y), jump])
            return moves
        else:
            return jumps

    def check_inbetween(self, start_x, start_y, middle_x, middle_y, jump_x, jump_y,
                        dx, dy):
        while True:
            start_x += dx
            start_y += dy
            if self.board[start_x][start_y] != '.':
                if start_x == middle_x and start_y == middle_y:
                    pass
                else:
                    return False
            if start_x == jump_x and start_y == jump_y:
                return True

    # checks if there's a piece on the start position mentioned
    # checks if the move is in the list of that players possible moves
    def check_not_legal(self, move):
        try:
            movelist = cif.to_coordinates(move, self.size)
        except IndexError:
            return True
        x, y = movelist[0][0], movelist[0][1]
        #print(x, y)
        if self.board[x][y] == '.':
            return True
        else:
            player = self.color_player_dict[self.board[x][y]]
            if player == self.current_turn:
                #print(movelist)
                #print(self.get_moves_piece([x,y]))
                if movelist in self.get_moves_piece([x,y]):
                    if player == self.current_turn:
                        return False
                
                else:
                    lbl = label(xoffset= 270,yoffset= -270, text="That's not a valid move",color=(1,0,0), border=4,height=12,font='monospace',line=0)
                    pause(lbl)
                    #print("that's not a valid move")
                    return True
            else:
                lbl = label(xoffset= 270,yoffset= -270, text="You're not that player",color=(1,0,0), border=4,height=12,font='monospace',line=0)
                pause(lbl)
                #print("you're not that player")
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
        board = deepcopy(self.board)
        i = 0
        for row in board:
            row.append(chr(ord('A') + i))
            i += 1

        first_row = []
        x = i
        while x > 0:
            first_row.append(str(x))
            x -= 1
        print_board = [first_row] + board

        for row in print_board:
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
    t0 = time()
    while halma_board.no_winner_yet():
        if not halma_board.test_run:
            halma_board.print_board()

        not_legal = True
        while not_legal:
            move = halma_board.current_turn.decide_move(halma_board)
            if move == 'check moves':
                moves = halma_board.get_moves_player(halma_board.current_turn)
                for move_int in moves:
                    move = cif.to_movestring(move_int, halma_board.size)
                    enemy = halma_board.get_next_player(halma_board.current_turn)
                    halma_board.make_move(move)
                    score = ABPlayer.alpha_beta(enemy, halma_board, -99999,
                                                99999, 1)
                    reverse_move(move, halma_board)
                    #print(move, score)
                #print('There are', len(moves), 'possible moves.')
            else:
                not_legal = halma_board.check_not_legal(move)
        #drawfile.draw(halma_board, move)
        halma_board.make_move(move)
        turn += 1
        halma_board.next_player()

    states = 0
    for player in halma_board.players:
        states += player.results(player.player_wins())

    winner = halma_board.who_won()
    t1 = time()
    #if not halma_board.test_run:
    if False:
        print("Congratulations!,", winner, "has won!")
        print("It took", str(int(t1 - t0)), "seconds, over", str(turn), "turns.")
        print()
    elif randint(0, 999) == 1 and halma_board.test_run:
        print(int(states * 100) / len(halma_board.players), '% of the states were in the database.')

    halma_board.reset_board()


# ==========================================
# ----- MONTE CARLO FUNCTIONS ARE HERE -----
def load_data(name='Database.txt'):
    """Return a dictionary out of the database file."""
    print('Reading the database file...')
    with open(name, "r") as file:
        string = file.read()

    print('Loading the contents...')
    index = 3
    data = {}
    count = 0
    while index < len(string):
        key, win, total, index = decipher(string, index)
        count += 1
        data[key] = [win, total]

    print('Loaded', count, 'states.')
    print()
    return data


def decipher(string, index):
    """These are the rules to being able to extract data from the database."""
    char = ''
    i_2 = index
    i_1 = index

    while char != '"':  # Find the board key
        i_2 += 1
        char = string[i_2]
    key = string[i_1:i_2]

    i_2 += 6
    i_1 = i_2
    while char != ',':  # Find the win value
        i_2 += 1
        char = string[i_2]
    win = int(string[i_1:i_2])

    i_2 += 2
    i_1 = i_2
    while char != ']':  # Find the total value
        i_2 += 1
        char = string[i_2]
    total = int(string[i_1: i_2])

    i_2 += 6
    return key, win, total, i_2


def reverse_move(move, board):
    """Return a move that negates the input move. This is used instead of
    deepcopying the board."""
    i = 1
    for char in move[1:]:
        if char.isalpha():
            break
        i += 1
    board.make_move(move[i:] + move[:i])


def store(name='Database.txt', data=None):
    """Reset the Database file and write all contents of the dictionary."""
    if not data:
        data = MCPlayer.data

    print("Saving data, don't quit the program now.")
    with open(name, 'w') as file:
        file.truncate(0)
        for key in data.keys():
            value = data[key]
            file.write('"""' + str(key) + '"""' + ': ' + str(value) + ',\n')
    print("Done, stored", len(data.keys()), "states to", name)
    print()


def merge_database(name1='Database1.text', name2='Database2.txt',
                   name3='Merged_Database.txt'):
    """Combine two Monte Carlo databases."""
    data = load_data(name=name1)

    print('Reading the second database file...')
    with open(name2, "r") as file:
        string = file.read()

    print('Merging the contents...')
    index = 3
    merge_count = 0
    new_count = 0
    while index < len(string):
        key, win, total, index = decipher(string, index)
        if key in data:
            [old_win, old_total] = data[key]
            data[key] = [old_win + win, old_total + total]
            merge_count += 1
        else:
            data[key] = [win, total]
            new_count += 1
    print('Success, merged', merge_count, 'and found', new_count, 'new states.')
    print()

    store(name=name3, data=data)


class MCPlayer(Player):
    data = None

    def __init__(self, i, size, rows, type):
        Player.__init__(self, i, size, rows, type)
        self.path = set()

        if MCPlayer.data == None:
            MCPlayer.data = load_data()

    def best_move(self, board):
        """Return the move that will result in a board with the highest
        win rate."""
        best_score = -1
        best_move = ""
        best_key = ''
        for move_int in board.get_moves_player(self):
            move = cif.to_movestring(move_int, board.size)
            board.make_move(move)
            key = self.board_to_key(board)
            score = self.get_win(key)

            if score > best_score and key not in self.path:
                best_score = score
                best_move = move
                best_key = key

            reverse_move(move, board)

        self.path.add(best_key)
        return best_move

    def board_to_key(self, board):
        """Convert the board to a key that the dictionary can use."""
        key = '\n'
        for row in board.board:
            for char in row:
                if char == self.color:
                    key += 'X'
                elif char == '.':
                    key += '.'
                else:
                    key += 'O'
            key += '\n'

        if self.color == 'b':
            rev_key = ''
            for char in key:
                rev_key = char + rev_key
            return rev_key
        return key

    def decide_move(self, board):
        """To improve learning, it sometimes makes a random move."""
        if randint(0, 9) == 9:
            return self.rand_move(board)
        return self.best_move(board)

    def get_win(self, key):
        """Return the win-percentage of a board setting."""
        value = MCPlayer.data.get(key)
        if value:
            return float(value[0]) / float(value[1])  # wins / total
        return 0.5 - float(self.get_total_manhattan()) / 10000.0  # Guideline

    def rand_move(self, board):
        """Return a random move between all allowed moves."""
        moves = board.get_moves_player(self)
        move = None
        key = None

        while key in self.path or not key:  # Never return to a previous board.
            i = randint(0, len(moves) - 1)
            move = cif.to_movestring(moves[i], board.size)
            board.make_move(move)
            key = self.board_to_key(board)
            reverse_move(move, board)

        return move

    def results(self, win):
        """Update all used board states."""
        new_states = 0
        old_states = 0
        for key in self.path:
            if key not in MCPlayer.data:
                MCPlayer.data[key] = [0, 0]
                new_states += 1
            else:
                old_states += 1

            value = MCPlayer.data[key]
            if win:  # If you win, the win value will increase.
                value[0] += 1
            value[1] += 1  # The total value always increases.

        self.path = set()
        return float(old_states) / float(new_states + old_states)


# -------------         -----------------------------------------
# -------------AlfaBeta -----------------------------------------
class ABPlayer(Player):
    test = 0

    def __init__(self, i, size, rows, type):
        Player.__init__(self, i, size, rows, type)
        self.depth = 2

    def decide_move(self, board):
        """Returns the move that is best according to the Alpha Beta function"""
        best_move = ''
        best_score = 99999
        if self.color == 'r':
            best_score = -99999
        enemy = board.get_next_player(self)

        red = -99999
        blue = 99999

        for move_int in board.get_moves_player(self):
            move = cif.to_movestring(move_int, board.size)
            board.make_move(move)
            score = ABPlayer.alpha_beta(enemy, board, red, blue,
                                        self.depth - 1)

            if self.color == 'r' and score > best_score:
                best_move = move
                best_score = score
            elif self.color == 'b' and score < best_score:
                best_move = move
                best_score = score

            reverse_move(move, board)
        return best_move

    @staticmethod
    def alpha_beta(player, board, red, blue, depth):
        """Return the score that is least harmful for the given move."""
        if depth == 0 or not board.no_winner_yet():  # Baseline
            return board.get_score()

        best_score = red
        enemy = board.get_next_player(player)
        if player.color == 'b':
            best_score = blue

        for move_int in board.get_moves_player(player):
            move = cif.to_movestring(move_int, board.size)
            board.make_move(move)
            score = ABPlayer.alpha_beta(enemy, board, red, blue,
                                        depth - 1)
            reverse_move(move, board)

            # Cut of branches that will never be reached.
            if player.color == 'r' and score > best_score:
                if score >= blue:
                    return blue
                best_score = score
                red = best_score

            elif player.color == 'b' and score < best_score:
                if score <= red:
                    return red
                best_score = score
                blue = best_score

        return best_score
def pause(lbl):
    while True:
        rate(100)
        if scene.mouse.events:
            m = scene.mouse.getevent()
            if m.click == 'left':
                lbl.visible = 0
                return
                

"""
halma_board = Board(2, 10, 5, ['ab', 'h'])
while True:
    for _ in range(1000):
        main_game_loop(halma_board)
    store()
"""
