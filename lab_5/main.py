class GameState:
    def __init__(self):
        self.board = [0] * 9
        self.player_a_moves = []
        self.player_b_moves = []
        self.current_player = 'A'

    def is_final(self):
        return len(self.player_a_moves) >= 3 or len(self.player_b_moves) >= 3 or sum(self.player_a_moves) + sum(
            self.player_b_moves) == 15

    def apply_move(self, move):
        if self.current_player == 'A':
            self.player_a_moves.append(move)
            self.board[move - 1] = move
            self.current_player = 'B'
        elif self.current_player == 'B':
            self.player_b_moves.append(move)
            self.board[move - 1] = move
            self.current_player = 'A'

    def generate_valid_moves(self):
        return [i + 1 for i, num in enumerate(self.board) if num == 0]

    def get_opposite_player_state(self):
        opposite_state = GameState()
        opposite_state.board = self.board.copy()
        opposite_state.player_a_moves = self.player_a_moves.copy()
        opposite_state.player_b_moves = self.player_b_moves.copy()
        opposite_state.current_player = 'A' if self.current_player == 'B' else 'B'
        return opposite_state

    def evaluate(self, player):
        if player == 'A':
            return len(self.player_a_moves) - len(self.player_b_moves)
        else:
            return len(self.player_b_moves) - len(self.player_a_moves)


def minimax(state, depth, is_max_player):
    if depth == 0 or state.is_final():
        return state.evaluate('B')

    if is_max_player:
        max_eval = float('-inf')
        for move in state.generate_valid_moves():
            new_state = state.get_opposite_player_state()
            new_state.apply_move(move)
            eval = minimax(new_state, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.generate_valid_moves():
            new_state = state.get_opposite_player_state()
            new_state.apply_move(move)
            eval = minimax(new_state, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def make_b_move_with_minmax(state, depth):
    max_eval = float('-inf')
    best_move = None
    for move in state.generate_valid_moves():
        new_state = state.get_opposite_player_state()
        new_state.apply_move(move)
        eval = minimax(new_state, depth, False)
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move


def play_game():
    game_state = GameState()
    while not game_state.is_final():
        if game_state.current_player == 'A':
            move = int(input(f'Jucatorul A, alege un numar intre 1 si 9: '))
            if move not in game_state.generate_valid_moves():
                print("Mutare invalida. Alege un numar disponibil.")
                continue
        else:
            print("Jucatorul B alege mutarea...")
            move = make_b_move_with_minmax(game_state, depth=2)
        game_state.apply_move(move)
        print(f"Jucator alege: {move}")
        print(f"Tabla de joc: {game_state.board}")
    if sum(game_state.player_a_moves) == 15:
        print("Jucatorul A a castigat!")
    elif sum(game_state.player_b_moves) == 15:
        print("Jucatorul B a castigat!")
    else:
        print("Remiza!")


if __name__ == '__main__':
    play_game()
