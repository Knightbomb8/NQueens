class ChessBoardNode:
    def __init__(self, state):
        # initialize initial values
        self.state = state
        self.conflicts = 0

        self.__calculate_conflicts()

    # determines how many conflicts the current chess board state has
    def __calculate_conflicts(self):
        state_length = len(self.state)
        for i in range(state_length * state_length):
            i_row = int(i / state_length)
            i_col = int(i % state_length)

            # if there is no queen here continue
            if self.state[i_row][i_col] == 0:
                continue

            for j in range(i + 1, state_length * state_length):
                j_row = int(j / state_length)
                j_col = int(j % state_length)

                # if there is no queen here continue
                if self.state[j_row][j_col] == 0:
                    continue

                # check if they are in same col, row, or are diagonal
                if i_col == j_col or i_row == j_row or abs(i_row - j_row) == abs(i_col - j_col):
                    self.conflicts += 1

    def __str__(self):
        message = ""
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                message += str(self.state[i][j]) + " "
            message += "\n"
        return message
