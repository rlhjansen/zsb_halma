"""from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *


"""
from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *
import wx
from copy import deepcopy
# from umi_common import *
# Custom made imports
# from umi_parameters import UMI_parameters
# from umi_chessboard import UMI_chessboard
# from umi_student_functions import *
import numpy as np
import os.path
from random import uniform, randint


# Returns notation [a1-h8] from coordinates
def to_coordinate(notation):
    """ Given a notation in the form [a1-h8], return the corresponding notation
        (0-7, 0-7)
        :param str notation: Location of a field on the board

        :return: Tuple internal coordinates of the field.
    """
    z = ord(notation[0]) - ord('a')
    x = int(notation[1]) - 1
    return (x, z)

def to_notation(coordinates):
    (x, z) = coordinates
    x += 7
    z += 7
    letter = chr(ord('a') + z)
    number = x + 1
    return letter + str(number)

def to_move(begin_position, end_position):
    move = ""
    move = move + begin_position + end_position
    return move

class UMI_chessboard:
    def __init__(self, frameworld, board_size=0.5, position_x_z=(0, 0)):
        # Dimensions of the board
        self.chessboard_size = board_size
        self.field_size = (self.chessboard_size / 16.0)

        # Edges of the locations
        self.wallthck = self.field_size / 30.0
        self.wallhght = self.field_size / 30.0

        # Position of the center of the board
        self.mplhght = (self.chessboard_size / 15.0)
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
        self.white_pieces_color = (1, 1, 1)
        self.black_pieces_color = (0, 0, 0)
        self.white_pieces_color = (1, 1, 1)

        # Set the frame of the chessboard.
        self.framemp = frame(frame=frameworld)
        self.framemp.pos = (-7.5, 0, -7.5)

        # Heights of the pieces:
        self.pieces_height = 0.3

        # Create the board on screen
        self.generate_board()

        # Add the pieces
        self.add_pieces()

        self.move_events()

# Generation of the checkerboard
    def generate_board(self):
        ''' Generates the visual display of the chessboard.
        '''
        self.mchessboard = box(frame=self.framemp,
                               height=self.mplhght,
                               length=self.chessboard_size,
                               width=self.chessboard_size,
                               pos=(0.5 * self.chessboard_size, -0.5 * self.mplhght, 0.5 * self.chessboard_size),
                               color=self.board_color_light)

        # Draw the beams to create 64 squares
        self.width_beams = []
        self.vert_beams = []
        for field in range(16):
            beam_offset = field * (self.chessboard_size / 16.0)
            self.width_beams.append(box(frame=self.framemp,
                                        height=self.wallhght,
                                        length=self.wallthck,
                                        width=self.mchessboard.width,
                                        pos=(beam_offset + (0.5 * self.wallthck), 0.5 * self.wallhght,
                                             0.5 * self.mchessboard.width),
                                        color=self.beam_color)
                                    )
            self.vert_beams.append(box(frame=self.framemp,
                                       height=self.wallhght,
                                       length=self.mchessboard.length,
                                       width=self.wallthck,
                                       pos=(0.5 * self.mchessboard.length, 0.5 * self.wallhght,
                                            beam_offset + (0.5 * self.wallthck)),
                                       color=self.beam_color)
                                   )
        self.width_beams.append(box(frame=self.framemp,
                                    height=self.wallhght,
                                    length=self.wallthck,
                                    width=self.mchessboard.width,
                                    pos=(self.chessboard_size - (0.5 * self.wallthck), 0.5 * self.wallhght,
                                         0.5 * self.mchessboard.width),
                                    color=self.beam_color)
                                )
        self.vert_beams.append(box(frame=self.framemp,
                                   height=self.wallhght,
                                   length=self.mchessboard.length,
                                   width=self.wallthck,
                                   pos=(0.5 * self.mchessboard.length, 0.5 * self.wallhght,
                                        self.chessboard_size - (0.5 * self.wallthck)),
                                   color=self.beam_color)
                               )

        self.fields = []
        for x in range(16):
            for z in range(16):
                if (x + z) % 2 == 0:
                    self.fields.append(box(frame=self.framemp,
                                           height=0.001,
                                           length=self.field_size,
                                           width=self.field_size,
                                           pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                                                (self.field_size * z) + self.field_size / 2),
                                           color=self.board_color_dark)
                                       )

    def move(self):
        # for piece in self.pieces:
        pick = None  # no object picked out of the scene yet
        switch = True
        while True:
            #rate(10)
            if scene.mouse.events:
                m1 = scene.mouse.getevent()  # get event
                if m1.press and m1.pick == piece and switch:  # if touched
                    drag_pos = m1.pickpos  # where on the ball
                    pick = m1.pick  # pick now true (not None)
                    switch = False
                elif m1.press and not switch:  # released at end of drag
                    switch = True
                    pick = None  # end dragging (None is false)
            if pick:
                closest = lambda s, d: s[0] - d[0]
                match = min(pieces, key=lambda p: closest(p, (piece.x, piece.y, piece.z)))
                new_pos = vector(match)
                if new_pos != drag_pos:
                    pick.pos = new_pos
                    drag_pos = new_pos

    def red_player(self, x, z):
        color_c = self.first_player_color
        color_n = "Red"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0.1 + 0.5 * self.wallhght,
                              (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[to_notation((4 - x, 4 - z))] = [piece, color_n]
        return

    def blue_player(self, x, z):
        color_c = self.second_player_color
        color_n = "Blue"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0.5 * self.wallhght,
                              (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[to_notation((x, z))] = [piece, color_n]
        return

    def green_player(self, x, z):
        color_c = self.third_player_color
        color_n = "Green"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                              (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[to_notation((x, z))] = [piece, color_n]
        return

    def yellow_player(self, x, z):
        color_c = self.fourth_player_color
        color_n = "Yellow"
        piece = cylinder(frame=self.framemp,
                         axis=(0, self.pieces_height, 0),
                         radius=self.field_size * 0.35,
                         pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                              (self.field_size * z) + self.field_size / 2),
                         color=color_c)
        self.pieces[to_notation((x, z))] = [piece, color_n]
        # print(to_notation((x, z)))
        return

    def get_piece(self, location):
        print("try to get the piece")
        print(location)

    def real_world_location(self, x, z):
        x+=7.5
        z+=7.5
        for a in range (17):
            if x < a and x > a-1:
                x = a - 0.5
            if z < a and z > a-1:
                z = a -0.5
        return (x,z)

    def move_piece(self, begin_location, end_location, obj):
        (x, z) = begin_location
        print((x,z))
        x_start = x-0.5
        y_start = z-0.5
        (x1, z1) = end_location
        print((x1, z1))
        x_end = x1-0.5 
        y_end = z1-0.5
        y = 0.1 + 0.5 *self.wallhght
        y1 = y
        if isinstance(obj, cylinder):
            obj.pos = (x1, y1, z1)
        return [[x_start, y_start], [x_end, y_end]]


    def move_events(self):
        piece = False
        while True:
            rate(10)
            mouse_event = scene.mouse.getevent()

            if mouse_event.press and piece == False:
                self.get_piece(mouse_event.pickpos)
                (x, y, z) = mouse_event.pickpos
                obj= mouse_event.pick
                print(obj)
                begin_location = self.real_world_location(x,z)
                #print((int(x+7.5), int(z+7.5)))
                #print(begin_location)
                piece = True
                print(piece)
            elif mouse_event.press and piece == True:
                self.get_piece(mouse_event.pickpos)
                (x, y, z) = mouse_event.pickpos
                end_location = self.real_world_location(x, z)
                #print(end_location)
                piece = False
                #move = to_move(begin_location, end_location)
                #print(move)
                self.move_piece(begin_location, end_location, obj)

                #mouse_event.pos = (x,y,z)
        return


                # m1 = scene.mouse.getevent()  # get event
                # if m1.press and m1.pick == piece and switch:  # if touched
                #     drag_pos = m1.pickpos  # where on the ball
                #     pick = m1.pick  # pick now true (not None)
                #     print(pick.pos)
                #     switch = False
                # elif m1.press and not switch:  # released at end of drag
                #     # m1.release = 'left'
                #     switch = True
                #     pick = None  # end dragging (None is false)

            # if pick:
            #     new_pos = scene.mouse.pickpos
            #     piecest = [(3, 0.2, 3), (4, 0.2, 3), (3, 0.2, 5)]
            #     closest = lambda s, d: s[0] - d[0]
            #     match = min(piecest, key=lambda p: closest(p, (pick.pos)))
            #     ne_pos = vector(match)
            #     if new_pos != drag_pos:  # if mouse has moved
            #         pick.pos += new_pos - drag_pos
            #         drag_pos = new_pos  # update drag position
            #         print(pick.pos)
            #         piecest = [(3, 0.2, 3), (4, 0.2, 3), (3, 0.2, 5)]
            #         closest = lambda s, d: s[0] - d[0]
            #         match = min(piecest, key=lambda p: closest(p, (pick.pos)))


        return

    def add_pieces(self):
        '''
        Adds and registers the pieces on the chessboard.
        '''
        self.pieces = dict()
        rows = 5
        size = 15
        pieces = []
        for z in range(0, 5):
            for x in [0, 1, 2, 3, 4]:
                if (x + z) < rows:
                    # color_c = self.first_player_color
                    # color_n = "Red"
                    # self.red_player(x,z)
                    color_c = self.first_player_color
                    color_n = "Red"
                    piece = cylinder(frame=self.framemp,
                                     axis=(0, self.pieces_height, 0),
                                     radius=self.field_size * 0.35,
                                     pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0.1 + 0.5 * self.wallhght,
                                          (self.field_size * z) + self.field_size / 2),
                                     color=color_c)
                    self.pieces[to_notation((4 - x, 4 - z))] = [piece, color_n]

                    #                    self.pieces[to_notation((4-x, 4-z))] = [piece, color_n]
                    #                    pieces.append(piece.pos)
                    #                    print(pieces)
                    #                    self.move()
                    #                    move(pieces, piece)
                    #                    scene.range = 3 # fixed size, no autoscaling
                    #                    ball = sphere(pos=(-3,0,0), color=color.cyan)
                    #                    cube = box(pos=(+3,0,0), size=(2,2,2), color=color.red)
                    #                    for i in pieces:
                    #                    for piece in self.pieces:
                    pick = None  # no object picked out of the scene yet
                    switch = True
        x_range = [size - x for x in range(rows)]
        z_range = [size - z for z in range(rows)]
        for x in x_range:
            for z in z_range:
                if 2 * size - rows < x + z:
                    self.blue_player(x, z)
                    # pieces.append(piece.pos)
                    # piecepos=piece.pos
                    # piece.pos.move()

        for x in x_range:
            for z in range(rows):
                if size - rows < x - z:
                    self.green_player(x, z)

        for x in range(rows):
            for z in z_range:
                if size - rows < z - x:
                    self.yellow_player(x, z)
                    # pieces.append(piece)
        return pieces
        # print(pieces)

        # print(pos)
        # print(self.pieces)


# return of action of the mouse

scene.width = 800
scene.height = 800
scene.title = "3D TicTacToe: 4 in a row"
# scene.center=(8,-8, 0)
# scene.center=(-.5,-.5, 0)
scene.forward = (0, -0.000001, 0)
# scene.autoscale=5

frameworld = frame()
# print(frameworld)
CHESSBOARD = UMI_chessboard(frameworld, 16, (-8, 8))
# alle locations in een lijst en beweegbaar maken






