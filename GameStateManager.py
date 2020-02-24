from random import randint
import random
import time
from Mouse import Mouse
import math
from MouseMoves import MouseMoves
from GameMap import GameMap
import GameState
from Canvas import Canvas
from CatManager import CatManager
from Cat import Cat
from Searches import Searches

class GameStateManager:
    def __init__(self, map_height=12, map_width=12, num_of_cheese=3):
        self.map_height = map_height
        self.map_width = map_width
        self.num_of_cheese = num_of_cheese
        self.visited_cheese_pos = []
        self.visited_mouse_pos = []
        self.visited_cat_pos = []
        self.game_states = []
        self.mouse_path = []
        self.mouse_initial_pos = []
        self.random_coordinates = []
        self.generate_resources()
        self.cheese_pos.sort(key=self.compare_by_distance)
        self.game_state = GameState.BasicGameState(self.mouse.current_pos, self.cat.current_pos, self.cheese_pos)
        self.game_states.append(self.game_state)
        self.game_map = GameMap(self.game_state, map_height, map_width)
        self.canvas = Canvas(self.game_map)

    def compare_by_distance(self, elem):
        return math.sqrt((math.pow(self.mouse.current_pos[0] - elem[0], 2)) + (math.pow(self.mouse.current_pos[1] - elem[1], 2)))

    def generate_unique_random_positions(self):
        randomX = -1
        randomY = -1
        random_positions = []
        while True:
            randomX = randint(0, self.map_width-1)
            randomY = randint(0, self.map_height-1)
            if [randomX, randomY] not in random_positions:
                random_positions.append([randomX, randomY])
            if (len(random_positions) == self.num_of_cheese + 2):
                return random_positions
        

    def generate_resources(self):
        unique_random_positions = self.generate_unique_random_positions()
        self.cheese_pos = []
        self.cheese_pos = [[5, 6], [1, 8], [1, 2]]
        self.cat = Cat([9, 4])
        self.mouse = Mouse([8, 11])

        # self.cheese_pos = [[6,0],[6,6],[4,9]]
        # self.cat = Cat([11,11])
        # self.mouse = Mouse([11,1])
        
        # for i in range(self.num_of_cheese + 2):
            
        #     if i < self.num_of_cheese:
        #         self.cheese_pos.append(unique_random_positions[i])
        #     elif i < self.num_of_cheese + 1:
        #         self.cat = Cat(unique_random_positions[i])
        #     else:
        #         self.mouse = Mouse(unique_random_positions[i])

    def run(self, search_type):
        self.move(search_type)


    def move(self, search_type):
        
        self.mouse_path = self.compute_mouse_path()

        self.search = Searches(self.mouse_path, self.game_map, self.cat)
        if search_type == "b":
            cat_path = self.search.breath_first_search()
        elif search_type == "d":
            cat_path = self.search.depth_first_search()
        else:
            cat_path = self.search.a_star_search()
        

        while len(cat_path) > 1:
            self.mouse.current_pos = self.mouse_path[1]
            if self.mouse_path[1] == self.cheese_pos[0]:
                self.visited_cheese_pos.append(self.cheese_pos.pop(0))
                self.cheese_pos = sorted(self.cheese_pos[:], key=self.compare_by_distance)
            self.visited_mouse_pos.append(self.mouse_path.pop(1))
            self.game_state = GameState.BasicGameState(self.mouse.current_pos, cat_path[1], self.cheese_pos)
            self.visited_cat_pos.append(cat_path.pop(1))
            self.game_map.update(self.game_state)
            self.canvas.display(self.game_map)
            print("Mouse Initial Position ", self.mouse.init_pos)
            print("Mouse visited position ", self.visited_mouse_pos)
            print("Cat visited position", self.visited_cat_pos)
            print("Visited Cheese Position ", self.visited_cheese_pos)

            time.sleep(1)

    def action(self, pos, move):
        new_location = pos[:]
        new_location[0] = new_location[0] + move.value[0]
        new_location[1] = new_location[1] + move.value[1]
        return new_location

    def compute_mouse_path(self):
        tmp_cheese_pos = self.cheese_pos[:]
        mouse_path = [self.mouse.current_pos]
        while len(tmp_cheese_pos) > 0:
            if tmp_cheese_pos[0][0] > mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] > mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.DOWN_RIGHT))
            elif tmp_cheese_pos[0][0] < mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] > mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.DOWN_LEFT))
            elif tmp_cheese_pos[0][0] > mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] < mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.UP_RIGHT))
            elif tmp_cheese_pos[0][0] < mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] < mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.UP_LEFT))
            elif tmp_cheese_pos[0][0] == mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] > mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.DOWN))
            elif tmp_cheese_pos[0][0] == mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] < mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.UP))
            elif tmp_cheese_pos[0][0] > mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] == mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.RIGHT))
            elif tmp_cheese_pos[0][0] < mouse_path[len(mouse_path)-1][0] and tmp_cheese_pos[0][1] == mouse_path[len(mouse_path)-1][1]:
                mouse_path.append(self.action(mouse_path[len(mouse_path)-1], MouseMoves.LEFT))
            if mouse_path[len(mouse_path)-1] == tmp_cheese_pos[0]:
                tmp_cheese_pos.pop(0)
                self.mouse.current_pos = mouse_path[len(mouse_path)-1]
                tmp_cheese_pos = sorted(tmp_cheese_pos[:], key=self.compare_by_distance)
        self.mouse.current_pos = self.mouse.init_pos
        return mouse_path