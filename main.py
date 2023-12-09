from collections import deque
import heapq
import time


# Reprezentarea Stării Problemei
def is_valid_move(state, row, col):
    empty_row, empty_col = find_empty_cell(state)
    return (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row)


def find_empty_cell(state):
    for i in range(3):
        for j in range(3):
            if state[i * 3 + j] == 0:
                return i, j


def make_move(state, row, col):
    empty_row, empty_col = find_empty_cell(state)
    new_state = state[:]
    new_state[empty_row * 3 + empty_col], new_state[row * 3 + col] = new_state[row * 3 + col], new_state[
        empty_row * 3 + empty_col]
    return new_state


# Stările Speciale și Funcțiile de Inițializare
def is_final_state(state):
    final_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return state == final_state


def initialize_problem(instance):
    return instance


# Strategia IDDFS (Iterative Deepening Depth-First Search)
def iddfs_search(instance):
    def depth_limited_search(state, depth, visited):
        if depth == 0:
            return None
        if is_final_state(state):
            return [state]

        visited.add(tuple(state))

        for i in range(3):
            for j in range(3):
                if is_valid_move(state, i, j):
                    new_state = make_move(state, i, j)
                    if tuple(new_state) not in visited:
                        result = depth_limited_search(new_state, depth - 1, visited)
                        if result is not None:
                            return [state] + result

        return None

    initial_state = initialize_problem(instance)
    max_depth = 1

    while True:
        visited = set()
        result = depth_limited_search(initial_state, max_depth, visited)
        if result is not None:
            return result
        max_depth += 1


# Strategia BFS (Breadth-First Search)
def bfs_search(instance):
    initial_state = initialize_problem(instance)
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        current_state, path = queue.popleft()

        if is_final_state(current_state):
            return path

        visited.add(tuple(current_state))

        for i in range(3):
            for j in range(3):
                if is_valid_move(current_state, i, j):
                    new_state = make_move(current_state, i, j)
                    if tuple(new_state) not in visited:
                        new_path = path + [(i, j)]
                        queue.append((new_state, new_path))

    return None


# Euristica 1: Distanța Manhattan
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i * 3 + j] != 0:
                correct_row, correct_col = (state[i * 3 + j] - 1) // 3, (state[i * 3 + j] - 1) % 3
                distance += abs(i - correct_row) + abs(j - correct_col)
    return distance


# Euristica 2: Distanța Hamming
def hamming_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0 and state[i] != i + 1:
            distance += 1
    return distance


# Euristica 3: Numărul de Celule în Poziție Greșită
def misplaced_cells(state):
    misplaced = 0
    for i in range(9):
        if state[i] != 0 and state[i] != i + 1:
            misplaced += 1
    return misplaced


# Strategia Greedy Search cu Euristici
def greedy_search(instance, heuristic):
    initial_state = initialize_problem(instance)
    visited = set()
    queue = [(heuristic(initial_state), initial_state)]

    while queue:
        _, current_state = heapq.heappop(queue)

        if is_final_state(current_state):
            return current_state

        visited.add(tuple(current_state))

        for i in range(3):
            for j in range(3):
                if is_valid_move(current_state, i, j):
                    new_state = make_move(current_state, i, j)
                    if tuple(new_state) not in visited:
                        heapq.heappush(queue, (heuristic(new_state), new_state))

    return None


# Implementarea Programului Principal
instances = [
    [8, 6, 7, 2, 5, 4, 0, 3, 1],
    [2, 5, 3, 1, 0, 6, 4, 7, 8],
    [2, 7, 5, 0, 8, 4, 3, 1, 6]
]

for i, instance in enumerate(instances):
    print(f"Instance {i + 1}: {instance}")
    print("==========================================")

    print("IDDFS:")
    start_time = time.time()
    iddfs_result = iddfs_search(instance)
    end_time = time.time()
    if iddfs_result:
        print(f"Solution found in {len(iddfs_result) - 1} moves")
        print(f"Execution time: {end_time - start_time} seconds")
    else:
        print("No solution found")

    heuristics = [manhattan_distance, hamming_distance, misplaced_cells]

    for heuristic in heuristics:
        print(f"Greedy Search with {heuristic.__name__}:")
        start_time = time.time()
        greedy_result = greedy_search(instance, heuristic)
        end_time = time.time()
        if greedy_result:
            print(f"Solution found in {heuristic(greedy_result)} heuristic score")
            print(f"Execution time: {end_time - start_time} seconds")
        else:
            print("No solution found")

    print("==========================================")
