class Player:
    # start and goal are integers like:
    # 0, 1, 2, 3 these represent corners as in start_positions.png
    # the corners are 4 diagonal rows from the corner, which consists of
    # a total of 9 pieces
    def __init__(self, number, size, rows):
        self.color = self.get_color(player)
        self.pieces = self.get_locations(player, size, rows)
        self.goal = self.end_loc(player, size)

    def end_location(self, player, size):



    def get_start_locations(self, number, size, rows):
        pieces = []
        if player == 0:
            for x in range(rows):
                for y in range(rows):
                    if x+y < rows:
                        pieces.append([x,y])

    def get_pieces(self):
        return self.pieces





