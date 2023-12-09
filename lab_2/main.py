import time
import queue


def initial_state(problem_instance):
    return problem_instance, None


def is_final_state(state):
    state_without_zeros = [x for x in state if x != 0]
    return all(state_without_zeros[i] == i + 1 for i in range(len(state_without_zeros)))


def generate_successor_states(state, last_move):
    successors = []
    empty_index = state.index(0)
    adjacent_indices = [empty_index - 1, empty_index + 1, empty_index - 3, empty_index + 3]

    for index in adjacent_indices:
        if 0 <= index < 9 and index != last_move:
            new_state = list(state)
            new_state[empty_index], new_state[index] = new_state[index], new_state[empty_index]
            successors.append((new_state, index))

    return successors


def custom_heuristic(state):
    # celule nu sunt in pozitia curenta
    misplaced = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != i + 1:
            misplaced += 1

    # nr de celule inversate
    inversion_penalty = 0
    for i in range(len(state) - 1):
        if state[i] != 0 and state[i + 1] != 0 and state[i] > state[i + 1]:
            inversion_penalty += 1

    # Valoarea euristicii este suma celor două măsurători
    return misplaced + inversion_penalty


def hamming_distance(state):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != i + 1:
            distance += 1
    return distance


def is_valid_transition(current_state, index):
    empty_index = current_state.index(0)
    return index in [empty_index - 1, empty_index + 1, empty_index - 3, empty_index + 3]


def iddfs(root_state, max_depth):
    initial_state, last_move = root_state, None
    for depth in range(max_depth + 1):
        result = dfs(initial_state, depth, last_move)
        if result:
            return result


def dfs(state, depth, last_move):
    initial_state = state
    if depth == 0:
        if is_final_state(state):
            return [state]
        return None

    for successor, move in generate_successor_states(state, last_move):
        result = dfs(successor, depth - 1, move)
        if result:
            return [initial_state] + result

    return None


def manhattan_distance(state):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            goal_x = (state[i] - 1) % 3
            goal_y = (state[i] - 1) // 3
            current_x = i % 3
            current_y = i // 3
            distance += abs(goal_x - current_x) + abs(goal_y - current_y)
    return distance


def greedy_best_first(init_state, heuristic_func):
    pq = queue.PriorityQueue()
    pq.put((heuristic_func(init_state), init_state))
    visited = set()

    while not pq.empty():
        _, state = pq.get()

        if is_final_state(state):
            return state
        # adauga vecini nevizitati pana cand caseste o solutie finala
        visited.add(tuple(state))
        for neighbor, _ in generate_successor_states(state, -1):
            if tuple(neighbor) not in visited:
                pq.put((heuristic_func(neighbor), neighbor))

    return None


def a_star(init_state, heuristic_func):
    pq = queue.PriorityQueue()
    g = {tuple(init_state): 0}
    pq.put((heuristic_func(init_state) + g[tuple(init_state)], init_state))
    visited = set()

    while not pq.empty():
        _, state = pq.get()

        if is_final_state(state):
            return state

        visited.add(tuple(state))
        for neighbor, move in generate_successor_states(state, -1):
            if tuple(neighbor) not in visited:
                g_neighbor = g[tuple(state)] + 1  # Costul real de la starea inițială
                if tuple(neighbor) not in g or g_neighbor < g[tuple(neighbor)]:
                    g[tuple(neighbor)] = g_neighbor
                    f_neighbor = g_neighbor + heuristic_func(neighbor)
                    pq.put((f_neighbor, neighbor))

    return None


def solution_length(solution):
    if solution:
        return len(solution) - 1
    return 0


instances = [[2, 5, 3, 1, 0, 6, 4, 7, 8], [2, 7, 5, 0, 8, 4, 3, 1, 6]]

for instance in instances:
    print(f"Instance: {instance}")
    for heuristic_func in [manhattan_distance, hamming_distance, custom_heuristic]:
        start_time = time.time()
        solution = greedy_best_first(instance, heuristic_func)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if solution:
            print(f"Heuristic: {heuristic_func.__name__}")
            print(f"Solution: {solution}")
            print(f"Length: {len(solution) - 1} moves")
            print(f"Execution Time: {elapsed_time} seconds")
        else:
            print(f"Heuristic: {heuristic_func.__name__}")
            print("No solution found")

    print("\n")

# instances = [[2, 5, 3, 1, 0, 6, 4, 7, 8], [2, 7, 5, 0, 8, 4, 3, 1, 6]]
#
# strategies = [
#     ("IDDFS", iddfs),
#     ("Greedy (Manhattan)", manhattan_distance),
#     ("Greedy (Hamming)", hamming_distance),
#     ("Greedy (Custom)", custom_heuristic),
#     ("A* (Manhattan)", manhattan_distance)
# ]
#
# for instance in instances:
#     print(f"Instance: {instance}")
#     for strategy_name, strategy_func in strategies:
#         start_time = time.time()
#         if strategy_name == "IDDFS":
#             solution = strategy_func(instance, 20)
#         else:
#             solution = a_star(instance, strategy_func)
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#
#         print(f"Strategy: {strategy_name}")
#         print(f"Solution: {solution}")
#         print(f"Length: {solution_length(solution)} moves")
#         print(f"Execution Time: {elapsed_time} seconds")
#         print("\n")
