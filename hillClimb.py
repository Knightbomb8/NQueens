from ChessBoardNode import ChessBoardNode
import copy
import time
from helpers import generate_random_board


def collect_n_queens_hill_climb_data(queen_count, boards_to_run):
    # counters for total search time and amount of boards searched
    total_search_time = 0
    total_boards_searched = 0
    solved_boards = 0

    for i in range(boards_to_run):
        # retrieve the returned values
        final_board, boards_searched, search_time, initial_board = n_queens_hill_climb(queen_count)
        # add search time and nodes searched to total
        total_search_time += search_time
        total_boards_searched += boards_searched
        if final_board.conflicts == 0:
            solved_boards += 1

    # compile the data and print it
    average_search_time = str(round(total_search_time / boards_to_run, 2))
    average_boards_explored = str(round(total_boards_searched / boards_to_run, 2))
    solved_percentage = str(round(solved_boards / boards_to_run * 100, 2)) + "%"

    # round our stats to two decimal places
    total_search_time = str(round(total_search_time, 2))
    total_boards_searched = str(round(total_boards_searched, 2))

    # print the stats out
    print("Out of", boards_to_run, "trials,", solved_boards, "(", solved_percentage, ") were successfully solved")
    print("With total search time of:", total_search_time, "ms averaging out to", average_search_time,
          "ms per n queens trial")
    print("With total boards explored of:", total_boards_searched, "boards averaging out to", average_boards_explored,
          "boards per n queens trial")


# runs an instance of n queens for hill climb
def n_queens_hill_climb(queen_count):
    board = generate_random_board(queen_count)

    # generate initial node
    cur_board = ChessBoardNode(board)
    initial_board = ChessBoardNode(board)

    # keep searching for a better node until we no longer find one
    keep_running = True
    # counter for total boards created starts at 1 as we made the initial board
    total_boards_searched = 1
    start_time = time.time()

    while keep_running:
        new_board, boards_searched = __find_best_child(cur_board)
        total_boards_searched += boards_searched

        # if the new board has less conflicts it is a valid continuation otherwise stop running
        if new_board.conflicts < cur_board.conflicts:
            cur_board = new_board
        else:
            keep_running = False

        # solution found
        if cur_board.conflicts == 0:
            keep_running = False

    # get time different in ms
    time_to_complete = (time.time() - start_time) * 1000

    # return completed board as well as stats to generate it
    return [cur_board, total_boards_searched, time_to_complete, initial_board]


# finds the best child board in hill climb steepest ascend
def __find_best_child(board):
    size = len(board.state)
    best_board = None
    boards_searched = 0

    # iterate over every column then create all possible next states
    for i in range(size):
        queen_row = -1
        for j in range(size):
            # determine where the one in the column is
            if board.state[j][i] == 1:
                queen_row = j
                break

        # now that we have the queen row set up all other possible states for the
        # next states to be
        for j in range(size):
            # if we are on the row the queen already exists at continue
            if j == queen_row:
                continue

            # generate a new state with the 1 here instead of original location
            new_state = copy.deepcopy(board.state)
            new_state[j][i] = 1
            new_state[queen_row][i] = 0

            # create a new board and add 1 to boards searched counter
            new_chess_board = ChessBoardNode(new_state)
            boards_searched += 1

            # check if its better
            if best_board is None or best_board.conflicts > new_chess_board.conflicts:
                # check if the board is solved, no point to keep searching
                if new_chess_board.conflicts == 0:
                    return [new_chess_board, boards_searched]
                best_board = new_chess_board

    return [best_board, boards_searched]
