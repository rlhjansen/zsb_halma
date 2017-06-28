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


class UMI_chessboard:
    def __init__(self, halma_board, frameworld, board_size=16.0):
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


    def make_move(self, move, size):
        coord_move = cl.cif.to_coordinates(move, size)
        [(y_start, x_start), (y_end, x_end)] = coord_move
        [obj, colour] = self.pieces[(x_start, y_start)]
        del self.pieces[(x_start, y_start)]
        self.pieces[(x_end, y_end)] = [obj, colour]
        end_location = (x_end + 1, y_end)
        (x1, z1) = end_location
        y1 = 0.1 + 0.5 * self.wallhght  # y is always the same, just above the board
        # only if the player has picked up a piece
        if isinstance(obj, cylinder):
            obj.pos = (x1-0.5, y1, z1+0.5)  # set to the new position
        else:
            pass


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
        for field in range(int(self.chessboard_size)):
            beam_offset = field * (self.chessboard_size / self.chessboard_size)
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
        for x in range(int(self.chessboard_size)):
            for z in range(int(self.chessboard_size)):
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
        return [begin_location, end_location]

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
    turn = 1
    t0 = cl.time()
    while halma_board.no_winner_yet():
        if True:
            halma_board.print_board()
            print()
            if halma_board.current_turn.color == 'r':
                color_n= "Red"
                lbl = label(xoffset= 320,yoffset= 320, text=color_n,color=(1,0,0), border=4,height=30,font='monospace',line=0)
            if halma_board.current_turn.color == 'b':
                color_n= "Blue"
                lbl = label(xoffset= 320,yoffset= 320, text=color_n,color=(0,0,1), border=4,height=30,font='monospace',line=0)
            if halma_board.current_turn.color == 'g':
                color_n= "Green"
                lbl = label(xoffset= 320,yoffset= 320, text=color_n,color=(0,100/255,0), border=4,height=30,font='monospace',line=0)
            if halma_board.current_turn.color == 'y':
                color_n= "Yellow"
                lbl = label(xoffset= 320,yoffset= 320, text=color_n,color=(1,1,0), border=4,height=30,font='monospace',line=0)
            print("turn", turn, halma_board.current_turn.color)
            print(halma_board.current_turn.get_total_manhattan())

        not_legal = True
        while not_legal:
            if halma_board.current_turn.type == 'h':
                movetype = 'm'
                if movetype == 'k':
                    move = raw_input("enter a move")
                    #move = halma_board.current_turn.decide_move(halma_board)
                    print(move)
                else:
                    board_move = CHESSBOARD.move_events()
                    [(x_start, y_start),(x_end, y_end)] = board_move
                    board_move2 = [(int(y_start-0.5), int(x_start-1.5)), (int(y_end-0.5), int(x_end-1.5))]
                    board_move3 = cl.cif.to_movestring(board_move2, halma_board.size)
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
                if not not_legal:
                    print(move)
                    CHESSBOARD.make_move(move, halma_board.size)
                    rate(100)

        halma_board.make_move(move)
        turn += 1
        halma_board.next_player()
        lbl.visible = 0

    states = 0
    for player in halma_board.players:
        states += player.results(player.player_wins())

    winner = halma_board.who_won()
    t1 = cl.time()
    lbl = label(yoffset=50, text="Congratulations! "+str(winner)+" has won!\n"+"It took "+str(int(t1 - t0))+" seconds, over "+str(turn)+" turns.\n"+str(int(states * 100) / len(halma_board.players))+'% of the states were in the database.',color=(30/255,144/255,1), border=4,height=30,font='monospace',line=0)
    cl.pause(lbl)
    lbl = label(yoffset=50, text="PLAY AGAIN",color=(30/255,144/255,1), border=4,height=30,font='monospace',line=0)
    cl.pause(lbl)
#     print("Congratulations!,", winner, "has won!")
#     print("It took", str(int(t1 - t0)), "seconds, over", str(turn), "turns.")
#     print(int(states * 100) / len(halma_board.players), '% of the states were in the database.')
#     print()
    halma_board.reset_board()

players = 2
boardsize = 6
rows = 3
playerlist = ['ab', 'ab']
halma_board = cl.Board(players, boardsize, rows, playerlist)
CHESSBOARD = UMI_chessboard(halma_board, frameworld, board_size=boardsize)
main_game_loop(halma_board)






