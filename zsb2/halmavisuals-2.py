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
#import wx
#from copy import deepcopy
#import numpy as np
#import os.path
#from random import uniform, randint


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

        # Pieces are able to move
        self.move_events()

# Generates the board in 3-D
    def generate_board(self):
        # Draw the white squares
        self.mchessboard = box(frame=self.framemp,
                               height=self.mplhght,
                               length=self.chessboard_size,
                               width=self.chessboard_size,
                               pos=(0.5 * self.chessboard_size, -0.5 * self.mplhght, 0.5 * self.chessboard_size),
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
        # Fill in the black squares
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

                    
    # Is used to convert the position of the mouse into a valid position on the board
    # (i.e. in the exact center of a square)
    def real_world_location(self, x, z):
        # 7.5 is added so the coordinates start at 0
        x+=7.5
        z+=7.5
        
        # Any position within one square is set to the exact center of that square
        for a in range (17):
            
            if x < a and x > a-1:
                x = a - 0.5
                
            if z < a and z > a-1:
                z = a -0.5
        return (x,z)
    

    # Currently doing: sets the piece that the player has picked up on its new position.
    # Should be doing: check if this is a legal move, if so it should be moved to its 
    # new position. If not, the piece should stay on its original position.
    def move_piece(self, begin_location, end_location, obj):
        (x, z) = begin_location
        (x1, z1) = end_location
        #print((x,z))
        #print((x1, z1))
        y = 0.1 + 0.5 *self.wallhght
        y1 = y # y is always the same, just above the board
        # Will be used for legal moves later
        x_start = x-0.5
        z_start = z-0.5      
        x_end = x1-0.5 
        z_end = z1-0.5
        
        # Rough idea for incorporating legal moves: !!!
        # if [[x_start, z_start], [x_end, z_end]] in legal moves:
        #   obj.pos = (x1, y1, z1) # new position
        # else:
        #   obj.pos = (x, y, z) # back to original position
        
        # only if the player has picked up a piece
        if isinstance(obj, cylinder): 
            obj.pos = (x1, y1, z1) # set to the new position
        else:
            pass
            
        return [[x_start, z_start], [x_end, z_end]]


    # Checks which object the player has clicked on
    def move_events(self):
        piece = False
        
        while True:
            rate(100)
            mouse_event = scene.mouse.getevent()

            if mouse_event.press and piece == False:
                (x, y, z) = mouse_event.pickpos # retrieve position of the mouse
                obj = mouse_event.pick # object that the player has clicked on is retrieved
                begin_location = self.real_world_location(x,z) 
                piece = True
                
            elif mouse_event.press and piece == True:
                (x, y, z) = mouse_event.pickpos # retrieve position of the mouse
                end_location = self.real_world_location(x, z)
                piece = False # piece is released
                self.move_piece(begin_location, end_location, obj) # moves the piece
        return



    # Makes the pieces in the different colors in their corresponding starting positions.
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
        return

    
    # Puts the pieces on the chessboard in their start position.
    def add_pieces(self):
        self.pieces = dict()
        rows = 5
        size = 15
        pieces = []
        
        # Upper-left corner
        for z in range(rows):
            for x in [0, 1, 2, 3, 4]:
                if (x + z) < rows:
                    self.red_player(x,z)
                    
        x_range = [size - x for x in range(rows)]
        z_range = [size - z for z in range(rows)]
        
        # Lower-right corner
        for x in x_range:
            for z in z_range:
                if 2 * size - rows < x + z:
                    self.blue_player(x, z)
                    
        # Upper-right corner
        for x in x_range:
            for z in range(rows):
                if size - rows < x - z:
                    self.green_player(x, z)
                    
        # Lower-left corner
        for x in range(rows):
            for z in z_range:
                if size - rows < z - x:
                    self.yellow_player(x, z)
        return pieces



# Settings of the display
scene.width = 800
scene.height = 800
scene.title = "Halma"
scene.forward = (0, -0.000001, 0)

frameworld = frame()
# Prints the board
CHESSBOARD = UMI_chessboard(frameworld, 16, (-8, 8))







