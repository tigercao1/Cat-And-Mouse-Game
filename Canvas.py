import time

class Canvas:
    def __init__(self, map):
        self.game_map = map
        self.display(self.game_map)

    def display(self, map):
        self.game_map = map
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                if (self.game_map.map[y][x] == 0):
                    print("⬜", end =" ")
                elif (self.game_map.map[y][x] == "c"):
                    print("🐱", end =" ")
                elif (self.game_map.map[y][x] == "m"):
                    print("🐭", end =" ")
                elif (self.game_map.map[y][x] == "e"):
                    print("🧀", end =" ")
                elif (self.game_map.map[y][x] == "v"):
                    print("😻", end =" ")
            print()
        print("\n\n")