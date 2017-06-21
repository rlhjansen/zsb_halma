
# translates a movestring, i.e. f4f3, to coordinate set i.e. [[
def to_coordinates(movestring):
    startpoints_x = []
    startpoints_y = []
    x_coords = []
    y_coords = []
    returnlist = []
    for i in range(len(movestring)):
        if not movestring[i].isdigit():
            startpoints_x.append(i)
        else:
            if startpoints_y == []:
                startpoints_y.append(i)
            elif startpoints_x[-1] > startpoints_y[-1]:
                startpoints_y.append(i)
    for i in startpoints_x:
        movestring[i].lower()
        x_coords.append(ord(movestring[i]) - ord('a'))
    for i in startpoints_y:
        temp_end = 0
        for number in startpoints_x:
            if i < number:
                temp_end = number
                break
        if temp_end == 0:
            temp_end = len(movestring)
        y_coords.append(int(movestring[i:temp_end]))
    for i in range(len(x_coords)):
        returnlist.append([x_coords[i], y_coords[i]])
    return returnlist

def to_movestring(move):
    movestring = ""
    for [x, y] in move:
        movestring += chr(ord('a')+x)
        movestring += str(y)
    return movestring

# returns the landing location after a jump
def get_jump_loc(x, y, new_x, new_y):
    land_x = x + (new_x - x)*2
    land_y = y + (new_y - y)*2
    return [land_x, land_y]


print(to_movestring([[1,2], [0,3], [1,3]]))
print(to_coordinates('b2a3b3'))