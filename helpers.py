import random


# generates a random n queens board of n size
def generate_random_board(size):
    # makes default array with no queens
    board = [[0 for i in range(size)] for j in range(size)]
    # for every row place a queen in a random location
    for i in range(size):
        board[random.randint(0, size - 1)][i] = 1
    # return the created board
    return board


# gets user input guaranteed to be an int in between min and max
def get_integer_input(minimum, maximum, message):
    selection = None
    # while we haven't properly gotten an int do keep going
    while selection is None:
        try:
            temp_selection = int(input(message))
            if minimum <= temp_selection <= maximum:
                selection = temp_selection
            else:
                print("Entered value must be >=", minimum, "and <=", maximum)
        except ValueError:
            print("Please enter a valid integer")
    # return the entered number
    return selection
