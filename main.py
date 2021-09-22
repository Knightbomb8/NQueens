from enum import Enum
from hillClimb import *
from minConflicts import *
from geneticAlgorithm import *
from helpers import get_integer_input


def main():
    # n queens algo information
    queen_count = 8
    boards_to_run = 1
    max_steps = 100
    max_generations = 250
    genetic_population_size = 250

    run_main = True

    # collect data
    # collect_n_queen_data(queen_count, boards_to_run, max_steps, max_generations, genetic_population_size)
    # run_main = False

    while run_main:
        message = "[1] to run n queen trials \n[2] to exit\n"
        # get the input
        selection = get_integer_input(1, 2, message)

        # if quitting
        if selection == 2:
            break

        print("Below algorithms are run with", queen_count, "queens\n")

        # otherwise run various puzzles
        # hill climb
        final_board, boards_searched, search_time, initial_board = n_queens_hill_climb(queen_count)
        solved = final_board.conflicts == 0
        print("Hill climb N queens result")
        print("_____________________________________________________________________")
        print("Initial Board:")
        print(initial_board)
        if solved:
            print("Solved in", str(round(search_time, 2)), "ms searching", boards_searched, "boards")
        else:
            print("Not solved in", str(round(search_time, 2)), "ms searching", boards_searched, "boards")
        print("Final Board:")
        print(final_board)
        print("\n")

        # min conflicts
        final_board, boards_searched, search_time, steps_taken, initial_board = n_queens_min_conflicts(queen_count,
                                                                                                       max_steps)
        solved = final_board.conflicts == 0
        print("Min Conflicts N queens result")
        print("_____________________________________________________________________")
        print("Initial Board:")
        print(initial_board)
        if solved:
            print("Solved in", str(round(search_time, 2)), "ms searching", boards_searched, "boards over",
                  steps_taken, "steps")
        else:
            print("Not solved in", str(round(search_time, 2)), "ms searching", boards_searched, "boards over",
                  steps_taken, "steps")
        print("Final Board:")
        print(final_board)
        print("\n")

        # genetic mutation
        final_board, search_time, generations_searched = n_queens_genetic_mutation(queen_count, genetic_population_size,
                                                                                   max_generations)
        solved = final_board.fitness == queen_count * (queen_count - 1) / 2
        print("Genetic Mutation N queens result")
        print("_____________________________________________________________________")
        total_boards = generations_searched * genetic_population_size;
        if solved:
            print("Solved in", str(round(search_time, 2)), "ms searching", total_boards, "boards over",
                  generations_searched, "generations")
        else:
            print("Not solved in", str(round(search_time, 2)), "ms searching", total_boards, "boards over",
                  generations_searched, "generations")
        print("Final Board:")
        print(final_board)
        print("\n")


# runs the various data collector for the n queen algos
def collect_n_queen_data(queen_count, boards_to_run, max_steps, max_generations, genetic_population_size):
    # # gathers hill climb data
    print("Data for the N Queens hill climb algorithm")
    print("-----------------------------------------------------------------")
    collect_n_queens_hill_climb_data(queen_count, boards_to_run)
    print("\n\n")

    # gather min conflicts data
    # print("Data for the N Queens min conflicts algorithm")
    # print("-----------------------------------------------------------------")
    # collect_n_queens_min_conflicts_data(queen_count, boards_to_run, max_steps)
    # print("\n\n")

    # gather genetic algo data
    # print("Data for the N Queens genetic algorithm")
    # print("-----------------------------------------------------------------")
    # collect_n_queens_genetic_mutation_data(queen_count, genetic_population_size, max_generations, boards_to_run)


# enum for current puzzle type being solved
class SolveType(Enum):
    STEEPEST_ASCENT = 1
    GENETIC = 2
    MIN_CONFLICTS = 3


if __name__ == '__main__':
    main()
