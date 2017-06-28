# Done:
# The board and the pieces all appear on the screen.
# You can pick up a piece by clicking on it.
# You can release the piece in another position by clicking on that position.
# After the piece is released, it should be moved to the exact center of a square.
# TO DO:
# The piece should only move if it's a legal move, if not, the piece should be sent
# back to its original position.
# Connect to the actual game.
# Write a function that makes it possible for the computer to move pieces.
# If there's time, make the game more user-friendly (start-buttons etc.)

from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *
import Classes as cl


# import wx
# from copy import deepcopy
# import numpy as np
# import os.path
# from random import uniform, randint


# Returns notation [a1-p16] from coordinates
def to_coordinate(notation):
    z = ord(notation[0]) - ord('a')
    x = int(notation[1]) - 1
    return (x, z)


# Returns coordinates from notation [a1-p16]
def to_notation(coordinates):
    (x, z) = coordinates
    x += 7
    z += 7
    letter = chr(ord('a') + z)
    number = x + 1
    return letter + str(number)


class UMI_chessboard2:
    def __init__(self, halma_board, frameworld, board_size=16.0, position_x_z=(0, 0)):
        self.halma_board_size = halma_board.size
        # Dimensions of the board
        self.chessboard_size = board_size
        self.field_size = (self.chessboard_size / (halma_board.size+1))

        # Edges of the locations
        self.wallthck = self.field_size / 30.0
        self.wallhght = self.field_size / 30.0

        # Position of the center of the board
        self.mplhght = (self.chessboard_size / (halma_board.size-1))
        # self.mplcent = (8,0,-8)
        self.mplcent = self.chessboard_size

        # Colors of the board
        self.board_color_light = (1.0, 1.0, 1.0)
        self.board_color_dark = (0, 0, 0)
        self.beam_color = (0.8, 0.8, 0.8)
        self.first_player_color = (255, 0, 0)
        self.second_player_color = (0, 0, 255)
        self.third_player_color = (0, 100, 0)
        self.fourth_player_color = (255, 255, 0)


        # Set the frame of the chessboard.
        self.framemp = frame(frame=frameworld)
        self.framemp.pos = (-(halma_board.size/2-0.5), 0, -(halma_board.size/2-0.5))

        # Heights of the pieces:
        self.pieces_height = 0.3

        # Create the board on screen
        self.generate_board()

        # Add the pieces
        self.add_pieces(halma_board)

        # Pieces are able to move

    # Generates the board in 3-D
    def generate_board(self):
        # Draw the white squares
        self.mchessboard = box(frame=self.framemp,
                               height=self.mplhght,
                               length=self.chessboard_size,
                               width=self.chessboard_size,
                               pos=(
                               0.5 * self.chessboard_size, -0.5 * self.mplhght,
                               0.5 * self.chessboard_size),
                               color=self.board_color_light)

        # Draw the beams to create 256 squares
        self.width_beams = []
        self.vert_beams = []
        for field in range(16):
            beam_offset = field * (self.chessboard_size / 16.0)
            self.width_beams.append(box(frame=self.framemp,
                                        height=self.wallhght,
                                        length=self.wallthck,
                                        width=self.mchessboard.width,
                                        pos=(
                                        beam_offset + (0.5 * self.wallthck),
                                        0.5 * self.wallhght,
                                        0.5 * self.mchessboard.width),
                                        color=self.beam_color)
                                    )
            self.vert_beams.append(box(frame=self.framemp,
                                       height=self.wallhght,
                                       length=self.mchessboard.length,
                                       width=self.wallthck,
                                       pos=(0.5 * self.mchessboard.length,
                                            0.5 * self.wallhght,
                                            beam_offset + (
                                            0.5 * self.wallthck)),
                                       color=self.beam_color)
                                   )
        self.width_beams.append(box(frame=self.framemp,
                                    height=self.wallhght,
                                    length=self.wallthck,
                                    width=self.mchessboard.width,
                                    pos=(self.chessboard_size - (
                                    0.5 * self.wallthck), 0.5 * self.wallhght,
                                         0.5 * self.mchessboard.width),
                                    color=self.beam_color)
                                )
        self.vert_beams.append(box(frame=self.framemp,
                                   height=self.wallhght,
                                   length=self.mchessboard.length,
                                   width=self.wallthck,
                                   pos=(0.5 * self.mchessboard.length,
                                        0.5 * self.wallhght,
                                        self.chessboard_size - (
                                        0.5 * self.wallthck)),
                                   color=self.beam_color)
                               )
        # Fill in the black squares
        self.fields = []
        for x in range(16):
            for z in range(16):
                if (x + z) % 2 == 0:
                    self.fields.append(box(frame=self.framemp,
                                           height=0.001,
                                           length=self.field_size,
                                           width=self.field_size,
                                           pos=(self.field_size * (
                                           x + 1) - self.field_size / 2.0, 0,
                                                (
                                                self.field_size * z) + self.field_size / 2),
                                           color=self.board_color_dark)
                                       )

    # Is used to convert the position of the mouse into a valid position on the board
    # (i.e. in the exact center of a square)
    def real_world_location(self, x, z):
        # 7.5 is added so the coordinates start at 0
        x += (self.halma_board_size+1)/2
        z += (self.halma_board_size-1)/2
        # Any position within one square is set to the exact center of that square
        for a in range(20):

            if x < a and x > a - 1:
                x = a - 0.5

            if z < a and z > a - 1:
                z = a - 0.5
        return (x, z)

    # Currently doing: sets the piece that the player has picked up on its new position.
    # Should be doing: check if this is a legal move, if so it should be moved to its
    # new position. If not, the piece should stay on its original position.
    def move_piece(self, end_location, obj):
        (x1, z1) = end_location
        y1 = 0.1 + 0.5 * self.wallhght # y is always the same, just above the board

        # only if the player has picked up a piece
        if isinstance(obj, cylinder):
            obj.pos = (x1, y1, z1)  # set to the new position
        else:
            pass

    # Checks which object the player has clicked on
    def move_events(self):
        piece = False
        begin_location = None
        end_location = None
        while True:
            mouse_event = scene.mouse.getevent()

            if mouse_event.press and piece == False:

                (x, y,
                 z) = mouse_event.pickpos  # retrieve position of the mouse
                obj = mouse_event.pick # object that the player has clicked on is retrieved
                if isinstance(obj, cylinder):
                    begin_location = self.real_world_location(x, z)
                    print(begin_location)
                    piece = True

            elif mouse_event.press and piece:
                (x, y,
                 z) = mouse_event.pickpos  # retrieve position of the mouse
                end_location = self.real_world_location(x, z)
                print(end_location)
                break
        return [begin_location, end_location, obj]

    # Makes the pieces in the different colors in their corresponding starting positions.
    def red_player(self, x, z):
        color_c = self.first_player_color
        color_n = "Red"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(
                         self.field_size * (x + 1) - self.field_size / 2.0,
                         0.1 + 0.5 * self.wallhght,
                         (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[(x, z)] = [piece, color_n]
        return

    def blue_player(self, x, z):
        color_c = self.second_player_color
        color_n = "Blue"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(
                         self.field_size * (x + 1) - self.field_size / 2.0,
                         0.5 * self.wallhght,
                         (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[(x, z)] = [piece, color_n]
        return

    def green_player(self, x, z):
        color_c = self.third_player_color
        color_n = "Green"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(
                         self.field_size * (x + 1) - self.field_size / 2.0, 0,
                         (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[(x, z)] = [piece, color_n]
        return

    def yellow_player(self, x, z):
        color_c = self.fourth_player_color
        color_n = "Yellow"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(
                         self.field_size * (x + 1) - self.field_size / 2.0, 0,
                         (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[(x, z)] = [piece, color_n]
        return

    # Puts the pieces on the chessboard in their start position.
    def add_pieces(self, halma_board):
        self.pieces = dict()
        rows = 5
        size = 15
        pieces = []
        for player in halma_board.players:
            pieces.extend(player.get_pieces())
        for [x, z] in pieces:
            colour = halma_board.board[x][z]
            if colour == 'r':
                self.red_player(x, z)
            elif colour == 'b':
                self.blue_player(x, z)
            elif colour == 'g':
                self.green_player(x, z)
            elif colour == 'y':
                self.yellow_player(x, z)



# Settings of the display
scene.width = 800
scene.height = 800
scene.title = "Halma"
scene.forward = (0, -0.000001, 0)

frameworld = frame()
# Prints the board

def main_game_loop(halma_board):
    rate(10)
    test_moves1 = ["a12a11","a11a10", "a10a9", "a9a8", "a8a7", "a7a6", "a6a5", "a5a4", "a4a3", "a3a2", "a2a1"]
    test_moves2 = ["p5p6", "p6p7", "p7p8", "p8p9", "p9p10", "p10p11", "p11p12", "p12p13", "p13p14", "p14p15", "p15p16"]
    test_moves = []
    for i in range(len(test_moves1)):
        test_moves.append(test_moves1[i])
        test_moves.append(test_moves2[i])
    iterable_moves = iter(test_moves)
    turn = 1
    t0 = cl.time()
    while halma_board.no_winner_yet():
        if True:
            halma_board.print_board()
            print()
            print("turn", turn, halma_board.current_turn.color)
            print(halma_board.current_turn.get_total_manhattan())

        not_legal = True
        while not_legal:
            if halma_board.current_turn.type == 'h':
                if turn<20 or 30<turn:
                    movetype = 'm'
                else:
                    movetype = raw_input("'k' for keyboard input, m for mouse input")
                if movetype == 'k':
                    move = "check moves"
                    #move = halma_board.current_turn.decide_move(halma_board)
                    print(move)
                else:
                    board_move = CHESSBOARD.move_events()
                    [(x_start, y_start),(x_end, y_end), obj] = board_move
                    end_location = (x_end-1, y_end)
                    board_move2 = [(int(y_start-0.5), int(x_start-1.5)), (int(y_end-0.5), int(x_end-1.5))]
                    print(board_move)
                    board_move3 = cl.cif.to_movestring(board_move2, halma_board.size)
                    board_move4 = cl.cif.to_coordinates(board_move3, halma_board.size)
                    print(board_move4)
                    [(y_start2, x_start2), (y_end2, x_end2)] = board_move4
                    print(CHESSBOARD.pieces[(y_start2, x_start2)][0])
                    second_obj = CHESSBOARD.pieces[(y_start2, x_start2)][0]
                    board_move5 = [(x_start2+1.5, y_start2+0.5), (x_end2+1.5, y_end2+0.5), second_obj]
                    print(board_move3)
                    print(board_move)
                    print(board_move5)
                    #move = iterable_moves.next()
                    move = board_move3
            else:
                move = halma_board.current_turn.decide_move(halma_board)
            if move == 'check moves':
                moves = halma_board.get_moves_player(halma_board.current_turn)
                for move in moves:
                    print(cl.cif.to_movestring(move, halma_board.size))
                print(len(moves))
            elif move == 'manhattan':
                print(halma_board.current_turn.get_total_manhattan())
            elif move == 'goalmanhattan':
                print(halma_board.current_turn.goal_manhattan)
            else:
                not_legal = halma_board.check_not_legal(move)
                if halma_board.current_turn.type == 'h' and not not_legal:
                    CHESSBOARD.move_piece(end_location, obj)
        #drawfile.draw(halma_board, move)
        halma_board.make_move(move)
        turn += 1
        halma_board.next_player()

    states = 0
    for player in halma_board.players:
        states += player.results(player.player_wins())

    winner = halma_board.who_won()
    t1 = time()
    print("Congratulations!,", winner, "has won!")
    print("It took", str(int(t1 - t0)), "seconds, over", str(turn), "turns.")
    print(int(states * 100) / len(halma_board.players), '% of the states were in the database.')
    print()
    halma_board.reset_board()


halma_board = cl.Board(2, 16, 5, ['h', 'h'])
#CHESSBOARD = UMI_chessboard(frameworld, 16, (-8, 8))
CHESSBOARD = UMI_chessboard2(halma_board, frameworld, 16, (-8, 8))

main_game_loop(halma_board)






