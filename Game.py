from GameStateManager import GameStateManager
from Mouse import Mouse
import Searches
import time

def main():
    game_over = False
    print("Game starting...")
    time.sleep(1)
    while game_over == False:
        game_state_manager = GameStateManager()
        file = open("current_game_initial_state.txt", "w")
        file.write("Cheese positions: " + str(game_state_manager.cheese_pos) + "\n")
        file.write("Cat position: " + str(game_state_manager.cat.init_pos) + "\n")
        file.write("Mouse Position: " + str(game_state_manager.mouse.init_pos))
        print("Calculating cat path according to mouse path...")
        print("Maximum", Searches.MAX_BLIND_SEARCHES, "searches for blind search")
        print("Maximum", Searches.MAX_INTELLIGENT_SEARCHES, "searches for a* search")
        game_state_manager.run("b")
        game_over = game_state_manager.game_map.game_over
        if game_over == False:
            print("Mouse won!")
            print("Number of searches:", game_state_manager.search.number_of_searches)
            print("Starting over....")
            time.sleep(2)
    print("Cat won!")
        
    print("Number of searches:", game_state_manager.search.number_of_searches)

main()
