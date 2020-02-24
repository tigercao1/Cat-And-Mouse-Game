import GameState
from CatManager import CatManager
import math

MAX_BLIND_SEARCHES = -1
MAX_INTELLIGENT_SEARCHES = -1

class Searches:
    def __init__(self, mouse_path, game_map, cat):
        self.number_of_searches = 0
        self.mouse_path = mouse_path
        self.cat = cat
        self.game_map = game_map
        self.cat_manager = CatManager(self.game_map)

    def depth_first_search(self):
        self.number_of_searches = 0
        cat_pos = self.cat.init_pos
        count = 0
        mouse_pos = self.mouse_path[count]
        dfs_stack = [GameState.BlindSearchGameState(self.mouse_path[count], cat_pos, None, 0)]
        cat_path = [cat_pos]
        visited_state = []
        while len(dfs_stack) > 0:
            self.number_of_searches += 1
            current_state = dfs_stack.pop(len(dfs_stack) - 1)
            count = current_state.move_count
            visited_state.append(current_state)
            possible_moves = self.cat_manager.get_all_possible_moves(current_state.cat)
            # print(self.number_of_searches)
            if len(possible_moves) > 0 and 0 <= count < len(self.mouse_path) - 1:
                game_state = None

                count += 1
                mouse_pos = self.mouse_path[count]
                
                for cat_pos in possible_moves:
                    game_state = GameState.BlindSearchGameState(mouse_pos, cat_pos, current_state, count)
                    if game_state not in visited_state:
                        dfs_stack.append(game_state)
            
            if current_state.cat == current_state.mouse_pos and not current_state.mouse_pos == self.mouse_path[len(self.mouse_path) - 1]:
                self.game_map.game_over = True
                break
            elif self.number_of_searches >= MAX_BLIND_SEARCHES and MAX_BLIND_SEARCHES != -1 and not current_state.cat == current_state.mouse_pos and current_state.mouse_pos == self.mouse_path[len(self.mouse_path) - 1]:
                break
                
        while not current_state.parent_state == None:
            cat_path.insert(1, current_state.cat)
            current_state = current_state.parent_state
        return cat_path

    def breath_first_search(self):
        self.number_of_searches = 0
        cat_pos = self.cat.init_pos
        count = 0
        mouse_pos = self.mouse_path[count]
        bfs_queue = [GameState.BlindSearchGameState(self.mouse_path[count], cat_pos, None, 0)]
        cat_path = [cat_pos]
        while len(bfs_queue) > 0:
            self.number_of_searches += 1
            current_state = bfs_queue.pop(0)
            count = current_state.move_count
            possible_moves = self.cat_manager.get_all_possible_moves(current_state.cat)
            # print(self.number_of_searches)
            if len(possible_moves) > 0 and 0 <= count < len(self.mouse_path) - 1:
                game_state = None

                count += 1
                mouse_pos = self.mouse_path[count]
                
                for cat_pos in possible_moves:
                    game_state = GameState.BlindSearchGameState(mouse_pos, cat_pos, current_state, count)
                    bfs_queue.append(game_state)
            
            if current_state.cat == current_state.mouse_pos and not current_state.mouse_pos == self.mouse_path[len(self.mouse_path) - 1]:
                self.game_map.game_over = True
                break
            elif self.number_of_searches >= MAX_BLIND_SEARCHES and MAX_BLIND_SEARCHES != -1:
                break

        while not current_state.parent_state == None:
            cat_path.insert(1, current_state.cat)
            current_state = current_state.parent_state
        return cat_path

    def a_star_search(self):
        self.number_of_searches = 0
        cat_pos = self.cat.init_pos
        count = 0
        mouse_pos = self.mouse_path[count]
        state_array = [GameState.IntelligentSearchGameState(self.mouse_path[count], cat_pos, None, 0, self.mouse_path)]
        closed_state_array = []
        cat_path = [cat_pos]
        while len(state_array) > 0:
            self.number_of_searches += 1
            state_array.sort(key=lambda x: x.cost)
            current_state = state_array.pop(0)
            if current_state not in closed_state_array:
                closed_state_array.append(current_state)
            count = current_state.move_count

            possible_moves = self.cat_manager.get_all_possible_moves(current_state.cat)
            # print(self.number_of_searches)
            if len(possible_moves) > 0 and 0 <= count < len(self.mouse_path) - 1:
                game_state = None
                count += 1
                mouse_pos = self.mouse_path[count]
                for cat_pos in possible_moves:
                    game_state = GameState.IntelligentSearchGameState(mouse_pos, cat_pos, current_state, count, self.mouse_path)
                    for state in state_array:
                        if state.mouse_pos == game_state.mouse_pos and state.cat == game_state.cat and not state.parent_state == game_state.parent_state and \
                            game_state.move_count < state.move_count:
                            state.parent_state = game_state.parent_state
                            state.update_cost(game_state.move_count)
                    for state in closed_state_array:
                        if state.mouse_pos == game_state.mouse_pos and state.cat == game_state.cat and not state.parent_state == game_state.parent_state and \
                            game_state.move_count < state.move_count:
                            state.parent_state = game_state.parent_state
                            state.update_cost(game_state.move_count)
                    if game_state not in state_array:
                        state_array.append(game_state)
                    current_state.add_children(game_state)
            
            if current_state.cat == current_state.mouse_pos and not current_state.mouse_pos == self.mouse_path[len(self.mouse_path) - 1]:
                self.game_map.game_over = True
                break
            elif self.number_of_searches >= MAX_INTELLIGENT_SEARCHES and MAX_INTELLIGENT_SEARCHES != -1:
                break

            # print(self.number_of_searches)
        while not current_state.parent_state == None:
            cat_path.insert(1, current_state.cat)
            current_state = current_state.parent_state
        return cat_path