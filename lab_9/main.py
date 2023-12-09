import numpy as np

num_rows = 7
num_cols = 10

initial_state = (3, 0)
goal_state = (3, 7)

Q_table = np.zeros((num_rows, num_cols, 4))

learning_rate = 0.1

discount_factor = 0.9

num_episodes = 1000

wind_strength = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice(4)
    else:
        return np.argmax(Q_table[state])


def apply_action(state, action):
    row, col = state

    if action == 0:
        row -= 1
    elif action == 1:
        row += 1
    elif action == 2:
        col -= 1
    elif action == 3:
        col += 1

    col += wind_strength[col]

    row = max(0, min(row, num_rows - 1))
    col = max(0, min(col, num_cols - 1))

    return (row, col)
