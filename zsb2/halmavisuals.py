from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *
import wx
from copy import deepcopy
import numpy as np
import os.path
from random import uniform, randint


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
    """ Given a board coordinate in the form (0-7, 0-7), return the corresponding notation
        [a1-h8]
        :param tuple coordinates: Tuple containing the internal coordinates on the board.

        :return: String in the form 'a1'
    """
    (x, z) = coordinates
    letter = chr(ord('a') + z)
    number = x + 1
    return letter + str(number)


class UMI_chessboard:
    def __init__(self, frameworld, board_size=16, position_x_z=(0, 0)):
        # Dimensions of the board
        self.chessboard_size = board_size
        self.field_size = (self.chessboard_size / 16.0)

        # Edges of the locations
        self.wallthck = self.field_size / 15.0
        self.wallhght = self.field_size / 15.0

        # Position of the center of the board
        self.mplhght = (self.chessboard_size / 15.0)
        # self.mplcent = (8,0,-8)
        self.mplcent = self.chessboard_size

        # Colors of the board
        self.board_color_light = (1.0, 1.0, 1.0)
        self.board_color_dark = (0, 0, 0)
        # self.beam_color = (0.9, 0.9, 0.9)
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
        self.framemp.pos = (-8, 0, -8)
        # self.framemp.pos =self.framemp.pos+vector(-0.5, -0.5)

        # Heights of the pieces:
        self.pieces_height = 0.02
        # Create the board on screen
        self.generate_board()

        # Add the pieces
        self.add_pieces()

        # Set the angle and position of the board, where the rotational axis is H8
        # self.set_pos_angle(position_x_z, 0)

    def remove_piece(self, position):
        '''
        Removes a piece from a stored location on the board, and return the object
        :param position: [a1-h8]
        :return: A VPython object (box/cylinder/pyramid)
        '''
        if position in self.pieces:
            piece_data = self.pieces.pop(position, None)
            return piece_data
        else:
            return None

    def get_board_height(self):
        ''' Gives the height of the board.
            :return: Returns the height of the board in meters.
        '''
        return self.mplhght

    def set_angle_radians(self, radians):
        ''' Sets the angle of the board, based of the corner next to h8
            :param radians: The angle of the board in radians.
        '''
        ## Rotate the board
        self.framemp.axis = (cos(radians), 0, sin(radians))
        # Used to read the radians of the board.
        self.board_angle = radians

    def set_angle_degrees(self, degrees):
        ''' Sets the angle of the board, based of the corner next to h8
            :param degrees: The angle of the board in degrees.
        '''
        self.set_angle_radians(radians(degrees))

    def get_angle_radians(self):
        ''' Gives the angle of the board in radians.
            :return: Returns the angle of the board in radians.
        '''
        return self.board_angle

    def get_angle_degrees(self):
        ''' Gives the angle of the board in degrees.
            :return: Returns the angle of the board in degrees.
        '''
        ## Rotate the board
        return degrees(self.get_angle_radians())

    def set_position(self, x, z):
        ''' Sets the horizontal position of the board, based of the corner next to h8
            :param x: The forward distance away from the robot arm
            :param z: The left/right distance away from the robot arm
        '''
        self.framemp.pos.x = x
        self.framemp.pos.z = z

    def get_position(self):
        ''' Returns a copy of the position (so students don't accidentally edit it)
            :param x: The forward distance away from the robot arm
            :return: Tuple containing the x, y and z coordinate.
        '''
        return (self.framemp.pos.x, self.framemp.pos.y, self.framemp.pos.z)

    def set_pos_angle(self, position_x_z, angle_degrees):
        ''' Sets the horizontal position of the board, and afterwards the angle based of the corner next to h8
            :param position_x_z: Tuple in the form (x, z)
            :param angle_degrees: The angle in degrees
        '''
        self.set_position(position_x_z[0], position_x_z[1])
        self.set_angle_degrees(angle_degrees)

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

    def add_pieces(self):
        '''
        Adds and registers the pieces on the chessboard.
        '''
        self.pieces = dict()
        rows = 5
        size = 15
        for z in range(0, 5):
            for x in [0, 1, 2, 3, 4]:
                if (x + z) < rows:
                    color_c = self.first_player_color
                    color_n = "Red"
                    piece = cylinder(frame=self.framemp,
                                     axis=(0, self.pieces_height, 0),
                                     radius=self.field_size * 0.35,
                                     pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                                          (self.field_size * z) + self.field_size / 2),
                                     color=color_c)
                    self.pieces[to_notation((4 - x, 4 - z))] = [piece, color_n]
        x_range = [size - x for x in range(rows)]
        z_range = [size - z for z in range(rows)]
        for x in x_range:
            for z in z_range:
                if 2 * size - rows < x + z:
                    color_c = self.second_player_color
                    color_n = "Blue"
                    piece = cylinder(frame=self.framemp,
                                     axis=(0, self.pieces_height, 0),
                                     radius=self.field_size * 0.35,
                                     pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                                          (self.field_size * z) + self.field_size / 2),
                                     color=color_c)
                    self.pieces[to_notation((x, z))] = [piece, color_n]
        for x in x_range:
            for z in range(rows):
                if size - rows < x - z:
                    color_c = self.third_player_color
                    color_n = "Green"
                    piece = cylinder(frame=self.framemp,
                                     axis=(0, self.pieces_height, 0),
                                     radius=self.field_size * 0.35,
                                     pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                                          (self.field_size * z) + self.field_size / 2),
                                     color=color_c)
                    self.pieces[to_notation((x, z))] = [piece, color_n]
        for x in range(rows):
            for z in z_range:
                if size - rows < z - x:
                    color_c = self.fourth_player_color
                    color_n = "Yellow"
                    piece = cylinder(frame=self.framemp,
                                     axis=(0, self.pieces_height, 0),
                                     radius=self.field_size * 0.35,
                                     pos=(self.field_size * (x + 1) - self.field_size / 2.0, 0,
                                          (self.field_size * z) + self.field_size / 2),
                                     color=color_c)
                    self.pieces[to_notation((x, z))] = [piece, color_n]
                    print(to_notation((x, z)))
                    # print(pos)

scene.width=800
scene.height=800
scene.title="3D TicTacToe: 4 in a row"
#scene.center=(8,-8, 0)
#scene.center=(-.5,-.5, 0)
scene.forward = (0,-0.1, 0)
scene.autoscale=0

frameworld = frame()
CHESSBOARD = UMI_chessboard(frameworld, 16, (0, 0))







