
# translates a movestring, i.e. f4a1, to coordinate set i.e. [[5,3],[0,0]]
def to_coordinates(movestring, boardsize):
    startpoints_x = []
    startpoints_y = []
    x_coords = []
    y_coords = []
    returnlist = []
    for i in range(len(movestring)):
        if not movestring[i].isdigit():
            startpoints_x.append(i)
        else:
            if not startpoints_y == []:
                if startpoints_x[-1] > startpoints_y[-1]:
                    startpoints_y.append(i)
            else:
                startpoints_y.append(i)
    for i in startpoints_x:
        x_coords.append(ord(movestring[i])-ord('a'))
    for i in range(len(startpoints_y)):
        print("yay")
        if startpoints_x[-1] > startpoints_y[i]:
            y_coords.append(boardsize - int(movestring[startpoints_y[i]:startpoints_x[i+1]])+1)
        else:
            y_coords.append(boardsize - int(movestring[startpoints_y[i]:])+1)
    for i in range(len(x_coords)):
        returnlist.append([y_coords[i], x_coords[i]])
    print(returnlist)
    return returnlist



def to_movestring(move, boardsize):
    movestring = ""
    for [x, y] in move:
        movestring += chr(ord('a')+x)
        movestring += str(boardsize - y+1)
    return movestring

def to_movestrings(moves, boardsize):
    move_list = []
    for move in moves:
        move_list.append(to_movestring(move, boardsize))
    return move_list

# returns the landing location after a jump
def get_jump_loc(x, y, new_x, new_y):
    land_x = x + (new_x - x)*2
    land_y = y + (new_y - y)*2
    return [land_x, land_y]


print(to_movestring([[1,2], [0,3], [1,3]], 10))
print(to_coordinates('a1a3a2', 10))