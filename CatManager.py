from Cat import Cat
from CatMoves import CatMoves

class CatManager:
    def __init__(self, map):
        self.map_height = map.height
        self.map_width = map.width
        self.visited_location = []

    def set_visited(self, pos):
        self.visited_location.append(pos)

    def in_boundary(self, pos):
        if pos[0] >= 0 and pos[0] < self.map_width and pos[1] >= 0 and pos[1] < self.map_height:
            return True
        return False

    def get_all_possible_moves(self, pos):
        move_set = []
        for moves in CatMoves:
            new_pos = [pos[0]+moves.value[0], pos[1]+moves.value[1]]
            if new_pos not in self.visited_location and self.in_boundary(new_pos):
                move_set.append(new_pos)
        return move_set