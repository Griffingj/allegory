from src.primitive import highest, lowest, compare
from src.chess.chess_movement import Move


class GameSearch():
    def __init__(self, score_state, next_actions, apply_action, undo_action, score_end):
        self.score_state = score_state
        self.next_actions = next_actions
        self.apply_action = apply_action
        self.undo_action = undo_action
        self.score_end = score_end
        self.move_count = 0

    # TODO figure out why this is so much slower
    # def alpha_beta_2(
    #             self,
    #             game_state,
    #             scan_depth,
    #             last_move,
    #             diag,
    #             ub=None,
    #             lb=None):

    #     # default to worse case
    #     high_cutoff = (highest * game_state.player_affinity() * -1, []) if ub is None else ub
    #     low_cutoff = (highest * game_state.player_affinity(), []) if lb is None else lb
    #     aff = game_state.player_affinity()
    #     self.move_count += 1

    #     if scan_depth == 0 or game_state.is_done:
    #         diag.count("leaf")
    #         return (self.score_state(game_state, last_move), [])
    #     else:
    #         best_outcome = (highest * aff * -1, [])  # default to worse case
    #         actions = self.next_actions(game_state)

    #         if not actions:
    #             diag.count("noActions")
    #             return (self.score_end(game_state), [])

    #         for action in actions:
    #             (new_state, undo) = self.apply_action(game_state, action)

    #             if aff == compare(best_outcome[0], high_cutoff[0]):
    #                 high_cutoff = best_outcome

    #             (next_score, critical_path) = self.alpha_beta_enh_r(
    #                 new_state,
    #                 scan_depth - 1,
    #                 action,
    #                 diag,
    #                 low_cutoff,
    #                 high_cutoff
    #             )
    #             new_state.undo(undo)

    #             if aff == compare(next_score, best_outcome[0]):
    #                 critical_path.append(action)
    #                 best_outcome = (next_score, critical_path)

    #             if aff * -1 == compare(low_cutoff[0], best_outcome[0]):
    #                 diag.count("prune")
    #                 break

    #         # if scan_depth == 3:
    #         #     print("-")

    #         return best_outcome

    def alpha_beta_enh_r(
            self,
            game_state,
            scan_depth,
            last_move,
            diag,
            alpha=(lowest, []),
            beta=(highest, [])):

        if scan_depth == 0 or game_state.is_done:
            diag.count("leaf")
            return (self.score_state(game_state, last_move), [])
        else:
            if game_state.player_affinity() == 1:
                max_best = (lowest, [])
                actions = self.next_actions(game_state)

                if not actions:
                    diag.count("noActions")
                    return (self.score_end(game_state), [])

                for action in actions:
                    (new_state, undo) = self.apply_action(game_state, action)
                    next_alpha = max_best if max_best[0] > alpha[0] else alpha

                    (next_score, critical_path) = self.alpha_beta_enh_r(
                        new_state,
                        scan_depth - 1,
                        action,
                        diag,
                        next_alpha,
                        beta
                    )
                    new_state.undo(undo)

                    if next_score > max_best[0]:
                        critical_path.append(action)
                        max_best = (next_score, critical_path)

                    if beta[0] <= max_best[0]:
                        diag.count("alphaPrune")
                        break

                return max_best
            else:
                min_best = (highest, [])
                actions = self.next_actions(game_state)

                if not actions:
                    diag.count("noActions")
                    return (self.score_end(game_state), [])

                for action in actions:
                    (new_state, undo) = self.apply_action(game_state, action)
                    next_beta = min_best if min_best[0] < beta[0] else beta

                    (next_score, critical_path) = self.alpha_beta_enh_r(
                        new_state,
                        scan_depth - 1,
                        action,
                        diag,
                        alpha,
                        next_beta
                    )
                    new_state.undo(undo)

                    if next_score < min_best[0]:
                        critical_path.append(action)
                        min_best = (next_score, critical_path)

                    if alpha[0] >= min_best[0]:
                        diag.count("betaPrune")
                        break

                return min_best
