from src.chess.chess_movement import get_moves

# Enhancements
# Static_Exchange_Evaluation https://www.chessprogramming.org/Static_Exchange_Evaluation
# Quiescence_Search https://www.chessprogramming.org/Quiescence_Search
#   see https://www.chessprogramming.org/Horizon_Effect
# Transposition Table https://www.chessprogramming.org/Transposition_Table
# Killer Heuristic https://www.chessprogramming.org/Killer_Heuristic
# Last_Best_Reply https://www.chessprogramming.org/Last_Best_Reply


def score_state(chess_state, search_state):
    # Enhancements https://www.chessprogramming.org/Evaluation#2015_...
    return chess_state.material_balance


def next_states(chess_state, search_state):
    return get_moves()

    return True
    # while num < n:
    #     yield num
    #     num += 1
