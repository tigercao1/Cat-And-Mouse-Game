import GameState
def main():
    test_state = GameState.BlindSearchGameState([1,1], [2,2], None, 5)
    test_state2 = GameState.BlindSearchGameState([1,1], [2,2], None, 5)
    print(test_state == test_state2)
    test_list = [test_state]
    test_list2 = [test_state]
    print (test_state2 in test_list)
    test_func(test_list)
    print(test_list[0].move_count)
    print(test_list2[0].move_count)

def test_func(list):
    list[0].move_count = 10
    for i in list:
        i.move_count = 20

main()
