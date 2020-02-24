class GameMap:
    def __init__(self, game_state, h, w):
        self.mouse_pos = game_state.mouse_pos
        self.cat_pos = game_state.cat
        self.cheese_pos = game_state.cheese
        self.height = h
        self.width = w
        self.map = []
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                self.map[y].append(0)
        self.map[self.mouse_pos[1]][self.mouse_pos[0]] = "m"
        self.map[self.cat_pos[1]][self.cat_pos[0]] = "c"
        self.game_over = False
        for pos in self.cheese_pos:
            self.map[pos[1]][pos[0]] = "e"

    def update(self, game_state):
        self.map = []
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                self.map[y].append(0)
        self.map[game_state.mouse_pos[1]][game_state.mouse_pos[0]] = "m"
        self.map[game_state.cat[1]][game_state.cat[0]] = "c"
        if (game_state.cat == game_state.mouse_pos):
            self.map[game_state.cat[1]][game_state.cat[0]] = "v"
        for pos in game_state.cheese:
            self.map[pos[1]][pos[0]] = "e"
            if (game_state.cat == pos):
                self.map[game_state.cat[1]][game_state.cat[0]] = "c"