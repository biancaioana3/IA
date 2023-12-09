def is_complete(assignment):
    for row in assignment:
        if None in row:
            return False
    return True


def next_unassigned_variable(assignment):
    for i in range(9):
        for j in range(9):
            if assignment[i][j] is None:
                return (i, j)
    return None


def is_even_constraint(assignment, row, col, num):
    if assignment[row][col] % 2 == 0:
        return num % 2 == 0
    return True


def is_valid_sudoku(assignment, row, col, value):
    for i in range(9):
        if assignment[row][i] == value or assignment[i][col] == value:
            return False

    region_row, region_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(region_row, region_row + 3):
        for j in range(region_col, region_col + 3):
            if assignment[i][j] == value:
                return False

    return True


def backtracking_with_forward_checking(assignment, domains):
    if is_complete(assignment):
        return assignment

    var = next_unassigned_variable(assignment)
    if var is None:
        return None

    row, col = var
    domain = domains[row][col]

    for value in domain:
        if is_valid_sudoku(assignment, row, col, value) and (
                assignment[row][col] != 0 or is_even_constraint(assignment, row, col, value)):
            new_assignment = [row.copy() for row in assignment]
            new_assignment[row][col] = value
            new_domains = [[dom.copy() for dom in row] for row in domains]

            for i in range(9):
                if i != col:
                    new_domains[row][i] = [x for x in new_domains[row][i] if x != value]
                if i != row:
                    new_domains[i][col] = [x for x in new_domains[i][col] if x != value]

            region_row, region_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(region_row, region_row + 3):
                for j in range(region_col, region_col + 3):
                    if i != row and j != col:
                        new_domains[i][j] = [x for x in new_domains[i][j] if x != value]

            if all(new_domains[i][j] for i in range(9) for j in range(9)):
                res = backtracking_with_forward_checking(new_assignment, new_domains)
                if res is not None:
                    return res

    return None


initial_board = [
    [8, 4, None, None, 5, None, 0, None, None],
    [3, None, None, 6, None, 8, None, 4, None],
    [None, None, 0, 4, None, 9, None, None, 0],
    [None, 2, 3, None, 0, None, 9, 8, None],
    [1, None, None, 0, None, 0, None, None, 4],
    [None, 9, 8, None, 0, None, 1, 6, None],
    [0, None, None, 5, None, 3, 0, None, None],
    [None, 3, None, 1, None, 6, None, None, 7],
    [None, None, 0, None, 2, None, None, 1, 3]
]

domains = [[list(range(1, 10)) if cell is None else [2, 4, 6, 8] if cell == 0 else [cell] for cell in row] for row in
           initial_board]

assignment = [row.copy() for row in initial_board]

solved_board = backtracking_with_forward_checking(assignment, domains)
if solved_board:
    for row in solved_board:
        print(row)
else:
    print("Nu există soluție.")
