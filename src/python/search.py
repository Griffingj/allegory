from src.python.chess.chess_consts import highest_score, lowest_score
from src.python.primitive import compare

low_default = (lowest_score, [])
high_default = (highest_score, [])
zero_score = (0, [])


class GameSearch():
    def __init__(self, score_state, next_actions, apply_action, undo_action, score_end, is_stop=False):
        self.score_state = score_state
        self.next_actions = next_actions
        self.apply_action = apply_action
        self.undo_action = undo_action
        self.score_end = score_end
        self.is_stop = is_stop
        self.best_outcome = None

    def stop(self, is_stop=True):
        self.is_stop = is_stop

    def iterative_deepening(
            self,
            game_state,
            max_depth,
            position_lookup,
            move_lookup,
            diag):

        for i in range(1, max_depth + 1):
            self.best_outcome = self.alpha_beta(
                game_state,
                i,
                i,
                None,
                position_lookup,
                move_lookup,
                diag
            )

        return self.best_outcome

    def alpha_beta(
            self,
            game_state,
            insight_depth,
            scan_depth,
            last_move,
            position_lookup,
            move_lookup,
            diag,
            alpha=low_default,
            beta=high_default):

        if self.is_stop:
            return zero_score

        if scan_depth == 0 or game_state.is_done:
            diag.count("leaf")
            return (self.score_state(game_state, last_move), [])
        else:
            if game_state.player_affinity() == 1:
                max_best = low_default

                for action in self.next_actions(game_state, move_lookup):
                    (new_state, undo) = self.apply_action(game_state, action)
                    next_alpha = max_best if max_best[0] > alpha[0] else alpha
                    key = (insight_depth, new_state.hash())
                    search_result = position_lookup.get(key, None)

                    if search_result is None:
                        search_result = self.alpha_beta(
                            new_state,
                            insight_depth,
                            scan_depth - 1,
                            action,
                            position_lookup,
                            move_lookup,
                            diag,
                            next_alpha,
                            beta
                        )
                        position_lookup[key] = search_result
                    else:
                        diag.count("position_lookup.cache_hit")

                    new_state.undo(undo)

                    if search_result[0] > max_best[0]:
                        search_result[1].append(action)
                        move_lookup["critical_path"].add(action)
                        max_best = search_result

                    if beta[0] <= max_best[0]:
                        move_lookup["pruners"].add(action)
                        diag.count("alpha_prune")
                        break

                if max_best == low_default:
                    diag.count("no_actions")
                    return zero_score

                return max_best
            else:
                min_best = high_default

                for action in self.next_actions(game_state, move_lookup):
                    (new_state, undo) = self.apply_action(game_state, action)
                    next_beta = min_best if min_best[0] < beta[0] else beta
                    key = (insight_depth, new_state.hash())
                    search_result = position_lookup.get(key, None)

                    if search_result is None:
                        search_result = self.alpha_beta(
                            new_state,
                            insight_depth,
                            scan_depth - 1,
                            action,
                            position_lookup,
                            move_lookup,
                            diag,
                            alpha,
                            next_beta
                        )
                        position_lookup[key] = search_result
                    else:
                        diag.count("position_lookup.cache_hit")

                    new_state.undo(undo)

                    if search_result[0] < min_best[0]:
                        search_result[1].append(action)
                        move_lookup["critical_path"].add(action)
                        min_best = search_result

                    if alpha[0] >= min_best[0]:
                        move_lookup["pruners"].add(action)
                        diag.count("beta_prune")
                        break

                if min_best == low_default:
                    diag.count("no_actions")
                    return zero_score

                return min_best

    # TODO figure out why this is so much slower
    def negamax(
            self,
            game_state,
            scan_depth,
            last_move,
            diag,
            ub=None,
            lb=None):

        if self.is_stop:
            return zero_score

        # default to worse case
        high_cutoff = (highest_score * -game_state.player_affinity(), []) if ub is None else ub
        low_cutoff = (highest_score * game_state.player_affinity(), []) if lb is None else lb
        aff = game_state.player_affinity()

        if scan_depth == 0 or game_state.is_done:
            diag.count("leaf")
            return (self.score_state(game_state, last_move), [])
        else:
            default = (highest_score * -aff, [])
            best_outcome = default  # default to worse case

            for action in self.next_actions(game_state):
                (new_state, undo) = self.apply_action(game_state, action)

                if aff == compare(best_outcome[0], high_cutoff[0]):
                    high_cutoff = best_outcome

                (next_score, critical_path) = self.negamax(
                    new_state,
                    scan_depth - 1,
                    action,
                    diag,
                    low_cutoff,
                    high_cutoff
                )
                new_state.undo(undo)

                if aff == compare(next_score, best_outcome[0]):
                    critical_path.append(action)
                    best_outcome = (next_score, critical_path)

                if -aff == compare(low_cutoff[0], best_outcome[0]):
                    diag.count("prune")
                    break

            if best_outcome == default:
                diag.count("no_actions")
                return zero_score

            return best_outcome
