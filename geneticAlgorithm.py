import random
import time


def collect_n_queens_genetic_mutation_data(num_queens, population_size, max_generations, boards_to_run):
    # counters for total search time and amount of boards searched
    total_search_time = 0
    total_boards_searched = 0
    solved_boards = 0
    total_generations_searched = 0

    for i in range(boards_to_run):
        # retrieve the returned values
        final_board, search_time, generations_searched = n_queens_genetic_mutation(num_queens, population_size,
                                                                                   max_generations)
        # add search time and nodes searched to total
        total_search_time += search_time
        total_boards_searched += generations_searched * population_size
        total_generations_searched += generations_searched
        if final_board.fitness == num_queens * (num_queens - 1) / 2:
            solved_boards += 1

    # compile the data and print it
    average_search_time = str(round(total_search_time / boards_to_run, 2))
    average_boards_explored = str(round(total_boards_searched / boards_to_run, 2))
    solved_percentage = str(round(solved_boards / boards_to_run * 100, 2)) + "%"
    average_generations_explored = str(round(total_generations_searched / boards_to_run, 2))

    # round our stats to two decimal places
    total_search_time = str(round(total_search_time, 2))
    total_boards_searched = str(round(total_boards_searched, 2))

    # print the stats out
    print("Out of", boards_to_run, "trials,", "with max generations of", max_generations, ",", solved_boards, "(",
          solved_percentage, ") were successfully solved")
    print("With total search time of:", total_search_time, "ms averaging out to", average_search_time,
          "ms per n queens trial")
    print("With total boards explored of:", total_boards_searched, "boards averaging out to", average_boards_explored,
          "boards per n queens trial")
    print("With total generations explored of:", total_generations_searched, "generations averaging out to ",
          average_generations_explored, "generations per n queens trial")


# runs an instance of the n queens problem using genetic mutation
def n_queens_genetic_mutation(num_queens, population_size, max_generations):
    # generate initial pool of population size nodes
    cur_population = []
    # start time
    start_time = time.time()

    for i in range(population_size):
        cur_population.append(GeneticAlgorithmNode(generate_random_state(num_queens)))

    generations = 1

    # while no solution keep running
    while True:
        # sort the current population
        # cur_population.sort(key=lambda x: x.fitness, reverse=True)
        weights = []
        best_node = None
        # get all the weights
        for i in cur_population:
            # hold the best node
            if best_node is None or best_node.fitness < i.fitness:
                best_node = i
            # probability of selecting this node as a parent
            weights.append(i.fitness * i.fitness)

        # if we have reached max generations or found an answer return it
        if generations >= max_generations or best_node.fitness == num_queens * (num_queens - 1) / 2:
            # get time different in ms
            time_to_complete = (time.time() - start_time) * 1000
            return [best_node, time_to_complete, generations]

        # add 1 to max generations made
        generations += 1

        new_population = []
        # generate a new population
        while len(new_population) < population_size:
            # grabs two parents weighted towards parents with a better fitness
            parent_a, parent_b = random.choices(cur_population, weights, k=2)
            # create random crossover point
            crossover_point = random.randint(0, num_queens)

            # containers for child a and b
            child_a_state = parent_a.state
            child_b_state = parent_b.state

            # if crossover is not 0 or num_queens, then we crossover otherwise they just equal the parents
            if crossover_point != 0 and crossover_point != num_queens:
                child_a_state = parent_a.state[:crossover_point] + parent_b.state[crossover_point:]
                child_b_state = parent_b.state[:crossover_point] + parent_a.state[crossover_point:]

            child_a = GeneticAlgorithmNode(child_a_state)
            child_b = GeneticAlgorithmNode(child_b_state)

            # TODO there will be times when we want to mutate multiple children
            # mutate teh children
            child_b = __mutate_state(child_b)
            child_a = __mutate_state(child_a)

            # append the new node
            new_population.append(child_a)
            # check if we have passed the needed length for new pop otherwise add the second node
            if len(new_population) < population_size:
                new_population.append(child_b)

        # assign the generated children as cur pop
        cur_population = new_population


# mutates a state with a given chance out of 100
def __mutate_state(genetic_node):
    # gets max fitness for current state
    best_fitness = len(genetic_node.state) * (len(genetic_node.state) - 1)

    # mutation chance goes up if there is a worse fitness
    mutation_chance = 100 / best_fitness * (best_fitness - genetic_node.fitness)

    # if we are below the given chance then switch a char out
    if random.randint(0, 100) < 15:
        original_state = genetic_node.state
        rand_pos = random.randint(0, len(original_state) - 1)
        new_state = original_state[:rand_pos] + str(random.randint(1, len(original_state) - 1)) + original_state[
                                                                                                  rand_pos + 1:]
        genetic_node = GeneticAlgorithmNode(new_state)
    return genetic_node


def generate_random_state(num_queens):
    state_string = ""
    # for every column generate random pos for the queen
    for i in range(num_queens):
        state_string += str(random.randint(1, num_queens))

    return state_string


# holds a state and fitness for a node
class GeneticAlgorithmNode:
    def __init__(self, state):
        self.state = state
        # higher number the better for fitness
        self.fitness = -1

        # calculate the fitness
        self.calculate_fitness()

    # determines the fitness for a given node
    def calculate_fitness(self):
        # determine conflicts
        int_state = self.get_state_as_list()
        num_conflicts = 0
        state_size = len(int_state)
        for i in range(state_size):
            for j in range(i + 1, state_size):
                # determine if diagonal or in same row
                if int_state[i] == int_state[j] or abs(int_state[j] - int_state[i]) == abs(i - j):
                    num_conflicts += 1

        # max possible conflicts minus num conflicts
        self.fitness = int((state_size * (state_size - 1) / 2) - num_conflicts)

    # returns the current state as a list of ints
    def get_state_as_list(self):
        char_state = [char for char in self.state]
        for i in range(len(char_state)):
            char_state[i] = int(char_state[i])

        return char_state

    # gets board state as a str
    def __str__(self):
        message = ""
        int_state = self.get_state_as_list()
        state_size = len(int_state)
        # make a 2d array
        for i in range(state_size):
            for j in range(state_size):
                if int_state[j] == i + 1:
                    message += "1 "
                else:
                    message += "0 "
            message += "\n"
        return message
