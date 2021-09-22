import random
from ChessBoardNode import ChessBoardNode
import copy
import time
from helpers import generate_random_board


# collects data for n queens min conflicts problems
def collect_n_queens_min_conflicts_data(queen_count, boards_to_run, max_steps):
    total_search_time = 0
    total_boards_searched = 0
    solved_boards = 0
    total_steps_taken = 0

    for i in range(boards_to_run):
        # retrieve the returned values
        final_board, boards_searched, search_time, steps_taken, initial = n_queens_min_conflicts(queen_count, max_steps)
        # add search time and nodes searched to total
        total_search_time += search_time
        total_boards_searched += boards_searched
        total_steps_taken += steps_taken
        if final_board.conflicts == 0:
            solved_boards += 1

    # compile the data and print it
    average_search_time = str(round(total_search_time / boards_to_run, 2))
    average_boards_explored = str(round(total_boards_searched / boards_to_run, 2))
    average_steps_taken = str(round(total_steps_taken / boards_to_run, 2))
    solved_percentage = str(round(solved_boards / boards_to_run * 100, 2)) + "%"

    # round our stats to two decimal places
    total_search_time = str(round(total_search_time, 2))
    total_boards_searched = str(round(total_boards_searched, 2))

    # print the stats out
    print("Out of", boards_to_run, "trials,", "with max step size of", max_steps, ",", solved_boards, "(",
          solved_percentage, ") were successfully solved")
    print("With total search time of:", total_search_time, "ms averaging out to", average_search_time,
          "ms per n queens trial")
    print("With total boards explored of:", total_boards_searched, "boards averaging out to", average_boards_explored,
          "boards per n queens trial")
    print("With total steps taken of:", total_steps_taken, "steps averaging out to ", average_steps_taken,
          "steps per n queens trial")


# runs an instance of n queens for min conflicts
def n_queens_min_conflicts(queen_count, max_steps):
    board = generate_random_board(queen_count)

    # generate initial node
    cur_board = ChessBoardNode(board)
    initial_board = ChessBoardNode(board)

    # var to hold total searched boards and steps taken
    total_boards_searched = 0
    steps_taken = max_steps

    # start time
    start_time = time.time()

    # run the algorithm for every step
    for i in range(max_steps):
        # check if the board is now solved then break
        if cur_board.conflicts == 0:
            steps_taken = i
            break

        # run a step of min conflicts
        cur_board, boards_searched = __run_min_conflicts_step(cur_board)
        total_boards_searched += boards_searched

    # get time different in ms
    time_to_complete = (time.time() - start_time) * 1000

    # return completed board as well as stats to generate it
    return [cur_board, total_boards_searched, time_to_complete, steps_taken, initial_board]


# runs a step for main conflicts
def __run_min_conflicts_step(board):
    # randomly choose a row to be the conflicted row
    board_width = len(board.state)
    conflicted_col = random.randint(0, board_width - 1)
    col_is_conflicted = False

    # check to make sure the random row is conflicted
    while not col_is_conflicted:
        # add 1 to the conflicted col every time to check the next col for a conflicted var
        conflicted_col = (conflicted_col + 1) % len(board.state)
        col_is_conflicted = is_col_conflicted(board, conflicted_col)
        pass

    # determine row of conflicted queen
    conflicted_row = -1
    # determine location of queen
    for i in range(board_width):
        if board.state[i][conflicted_col] == 1:
            conflicted_row = i

    best_board = None
    # default is that every possible search happens
    boards_searched = board_width - 1

    # determine the least conflicted next state for the conflicted queen
    for i in range(board_width):
        # if its the same row as the current node then continue as we don't want to repeat current state
        if conflicted_row == i:
            continue
        # create a new chess board node for every possible movement along the col
        new_state = copy.deepcopy(board.state)
        new_state[i][conflicted_col] = 1
        new_state[conflicted_row][conflicted_col] = 0

        # create the node
        new_chess_board = ChessBoardNode(new_state)

        # check if its better
        if best_board is None or best_board.conflicts > new_chess_board.conflicts:
            best_board = new_chess_board
            # check if solved
            if best_board.conflicts == 0:
                boards_searched = i + 1
                break

    return [best_board, boards_searched]


# determines if a specific row is conflicted
def is_col_conflicted(board, conflicted_col):
    conflicted_row = -1
    board_width = len(board.state)
    # determine location of queen
    for i in range(board_width):
        if board.state[i][conflicted_col] == 1:
            conflicted_row = i

    # check if it has any conflicts
    for i in range(board_width * board_width):
        i_row = int(i / board_width)
        i_col = int(i % board_width)

        # if the spot we are checking is in the same col then continue
        if i_col == conflicted_col:
            continue

        # check if its 1 and if so check for a conflict
        if board.state[i_row][i_col] == 1:
            # check if they are in same col, row, or are diagonal then we are conflicting so return true
            if i_col == conflicted_col or i_row == conflicted_row or abs(i_row - conflicted_row) == \
                    abs(i_col - conflicted_col):
                return True

    # if we get here, it means no conflicts thus we return False
    return False
