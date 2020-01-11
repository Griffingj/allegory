from src.primitive import lowest, highest


def minimax(game_state, next_actions, score_state, apply_action, search_depth, maxer=True):
    if search_depth == 0 or game_state.is_done:
        return score_state(game_state)
    else:
        scores = [lowest if maxer else highest]

        for action in next_actions(game_state):
            (new_state, undo) = apply_action(game_state, action)
            next_score = minimax(
                new_state,
                next_actions,
                score_state,
                apply_action,
                search_depth - 1,
                not maxer
            )
            scores.append(next_score)

        return max(scores) if maxer else min(scores)


def alpha_beta_basic(
        game_state,
        next_actions,
        score_state,
        apply_action,
        scan_depth,
        max_prior_best=(lowest, None),
        min_prior_best=(highest, None)):

    if scan_depth == 0 or game_state.is_done:
        return (score_state(game_state), None)
    else:
        if game_state.is_maxer:
            max_best = (lowest, None)

            for action in next_actions(game_state):
                (new_state, undo) = apply_action(game_state, action)
                alpha_meta = max_best if max_best[0] > max_prior_best[0] else max_prior_best

                (next_score, pos) = alpha_beta_basic(
                    new_state,
                    next_actions,
                    score_state,
                    apply_action,
                    scan_depth - 1,
                    alpha_meta,
                    min_prior_best
                )
                if next_score > max_best[0]:
                    max_best = (next_score, action)

                if min_prior_best[0] <= max_best[0]:
                    # Avoiding searching (pruning) the rest of the moves and their descendents
                    # because max_best is higher than miner's prior best option. Don't have to look
                    # further if this is the case because on a prior move, miner will prefer
                    # lower alternative
                    return max_best
            return max_best
        else:
            min_best = (highest, None)

            for action in next_actions(game_state):
                (new_state, undo) = apply_action(game_state, action)
                beta_meta = min_best if min_best[0] < min_prior_best[0] else min_prior_best

                (next_score, pos) = alpha_beta_basic(
                    new_state,
                    next_actions,
                    score_state,
                    apply_action,
                    scan_depth - 1,
                    max_prior_best,
                    beta_meta
                )
                if next_score < min_best[0]:
                    min_best = (next_score, action)

                if max_prior_best[0] >= min_best[0]:
                    return min_best
            return min_best


class GameSearch():
    def __init__(self, score_state, next_actions, apply_action, undo_action, score_end, is_winning_action):
        self.score_state = score_state
        self.next_actions = next_actions
        self.apply_action = apply_action
        self.undo_action = undo_action
        self.score_end = score_end
        self.is_winning_action = is_winning_action
        self.critical_path = [None] * 30
        self.path = [None] * 30

    def alpha_beta_enh_r(
            self,
            game_state,
            scan_depth,
            initial_depth,
            diag,
            alpha=(lowest, None),
            beta=(highest, None)):

        d = initial_depth - scan_depth

        if scan_depth == 0 or game_state.is_done:
            diag.count("leaf")
            # idx = d - 2
            # last_action_same_side = self.path[idx] if idx > 0 else None
            return (self.score_state(game_state), None)
        else:
            if game_state.is_maxer:
                max_best = (lowest, None)
                actions = self.next_actions(game_state)

                if not actions:
                    diag.count("noActions")
                    return (self.score_end(game_state), None)

                for action in actions:
                    (new_state, undo) = self.apply_action(game_state, action)
                    self.path[d] = action

                    if self.is_winning_action(action):
                        return (highest, action)

                    next_alpha = max_best if max_best[0] > alpha[0] else alpha

                    (next_score, _) = self.alpha_beta_enh_r(
                        new_state,
                        scan_depth - 1,
                        initial_depth,
                        diag,
                        next_alpha,
                        beta
                    )
                    new_state.undo(undo)

                    if next_score > max_best[0]:
                        max_best = (next_score, action)

                    if beta[0] <= max_best[0]:
                        diag.count("alphaPrune")
                        break

                self.critical_path[d] = max_best[1]
                return max_best
            else:
                min_best = (highest, None)
                actions = self.next_actions(game_state)

                if not actions:
                    diag.count("noActions")
                    return (self.score_end(game_state), None)

                for action in self.next_actions(game_state):
                    (new_state, undo) = self.apply_action(game_state, action)
                    self.path[d] = action

                    if self.is_winning_action(action):
                        return (lowest, action)

                    next_beta = min_best if min_best[0] < beta[0] else beta

                    (next_score, _) = self.alpha_beta_enh_r(
                        new_state,
                        scan_depth - 1,
                        initial_depth,
                        diag,
                        alpha,
                        next_beta
                    )
                    new_state.undo(undo)

                    if next_score < min_best[0]:
                        min_best = (next_score, action)

                    if alpha[0] >= min_best[0]:
                        diag.count("betaPrune")
                        break

                self.critical_path[d] = min_best[1]
                return min_best
