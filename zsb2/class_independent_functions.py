def to_coordinates(movestring):
    startpoints = []
    for i in range(len(movestring)):
        if ord(movestring[i]) > 64:
            startpoints.append(i)



def get_jump_loc(x, y, new_x, new_y):
    land_x = x + (new_x - x)*2
    land_y = y + (new_y - y)*2
    return [land_x, land_y]