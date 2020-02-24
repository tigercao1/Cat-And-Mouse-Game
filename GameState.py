from GameMap import GameMap
import math
import GameStateManager

class BasicGameState:
    def __init__(self, mouse_pos, cat, cheese):
        self.mouse_pos = mouse_pos
        self.cat = cat
        self.cheese = cheese

    def __eq__(self, other):
        if other == None:
            return False
        return self.mouse_pos == other.mouse_pos and self.cat == other.cat and self.cheese == other.cat

class BlindSearchGameState(BasicGameState):
    def __init__(self, mouse_pos, cat, parent_state, move_count):
        BasicGameState.__init__(self, mouse_pos, cat, [])
        self.parent_state = parent_state
        self.move_count = move_count

    def __eq__(self, other):
        if other == None:
            return False
        return self.mouse_pos == other.mouse_pos and self.cat == other.cat and self.cheese == other.cat and self.parent_state == other.parent_state and self.move_count == other.move_count

class IntelligentSearchGameState(BlindSearchGameState):
    def __init__(self, mouse_pos, cat, parent_state, move_count, mouse_path):
        BlindSearchGameState.__init__(self, mouse_pos, cat, parent_state, move_count)
        self.mouse_path = mouse_path
        self.estimate = self.heuristic1()
        self.cost = self.move_count + self.estimate
        self.children = []
        
    def __eq__(self, other):
        if other == None:
            return False
        return self.mouse_pos == other.mouse_pos and self.cat == other.cat and self.cheese == other.cat and self.parent_state == other.parent_state and self.move_count == other.move_count and self.estimate == other.estimate and self.cost == other.cost

    def update_cost(self, move_count):
        self.move_count = move_count
        self.cost = move_count + self.estimate
        self.update_children_cost(self)

    def update_children_cost(self, game_state):
        if len(game_state.children) == 0:
            return
        else:
            for state in game_state.children:
                state.move_count = self.move_count
                game_state.cost = state.move_count + state.estimate
                self.update_children_cost(state)
            
    def add_children(self, child_state):
        self.children.append(child_state)
    
    # Calculating the euclidean distance of the cat position relative to the mouse position at each state(where whenever mouse moves, cat moves)
    # and divide that by 2 since cat moves around 2 blocks each time to ensure our heuristic function does not overestimate
    def heuristic1(self):
        return math.sqrt((math.pow(self.cat[0] - self.mouse_pos[0], 2)) + (math.pow(self.cat[1] - self.mouse_pos[1], 2)))/2

    # Calculating the euclidean distance of the cat position to the center of all of the mouse position coordinates
    # divide the value by 2 since cat moves around 2 block each time to ensure our heuristic function does not overestimate
    def heuristic2(self):
        mouse_path = self.mouse_path
        center_of_x = sum(m[0] for m in mouse_path)/len(mouse_path)
        center_of_y = sum(m[1] for m in mouse_path)/len(mouse_path)
        return math.sqrt((math.pow(self.cat[0] - center_of_x, 2)) + (math.pow(self.cat[1] - center_of_y, 2)))/3

    def heuristic3(self):
        return (self.heuristic1() + self.heuristic2())/3


    


