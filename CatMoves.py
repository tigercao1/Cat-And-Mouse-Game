from enum import Enum
class CatMoves(Enum):
    UP_LEFT = [-1, -2]
    UP_RIGHT = [1, -2]
    RIGHT_UP = [2, -1]
    RIGHT_DOWN = [2, 1]
    DOWN_LEFT = [-1, 2]
    DOWN_RIGHT = [1, 2]
    LEFT_UP = [-2, -1]
    LEFT_DOWN = [-2, 1]