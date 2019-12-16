from primitive import set_

lb = float("-inf")
ub = float("inf")


class GameSearch():
    def __init__(self, score_state, next_states):
        self.score_state = score_state
        self.next_states = next_states

    def minimax(self, state, search_depth=5, maxer=True):
        if search_depth == 0 or state.is_done:
            return self.score_state(state)
        else:
            scores = [lb if maxer else ub]

            for new_state in self.next_states(state):
                next_score = self.minimax(
                    new_state,
                    search_depth - 1,
                    not maxer
                )
                scores.append(next_score)

            return max(scores) if maxer else min(scores)

    def alpha_beta(
            self,
            state,
            search_depth=5,
            max_prior_best=lb,
            min_prior_best=ub,
            maxer=True):

        if search_depth == 0 or state.is_done:
            return self.score_state(state)
        else:
            if maxer:
                max_best = lb

                for new_state in self.next_states(state):
                    next_score = self.alpha_beta(
                        new_state,
                        search_depth - 1,
                        max(max_best, max_prior_best),
                        min_prior_best,
                        not maxer
                    )
                    max_best = max(max_best, next_score)
                    if min_prior_best <= max_best:
                        # Avoiding searching (pruning) the reset of the moves and their descendents
                        # because max_best is higher than miner's prior best option. Don't have to look
                        # further if this is the case because on a prior move, miner will prefer
                        # lower alternative
                        return max_best
                return max_best
            else:
                min_best = ub

                for new_state in self.next_states(state):
                    next_score = self.alpha_beta(
                        new_state,
                        search_depth - 1,
                        max_prior_best,
                        min(min_best, min_prior_best),
                        not maxer
                    )
                    min_best = min(min_best, next_score)
                    if max_prior_best >= min_best:
                        return min_best
                return min_best

    def alpha_beta_max(
            self,
            game_state,
            search_state,
            scan_depth=5,
            max_prior_best=[lb, None],
            min_prior_best=[ub, None]):

        g_d = search_state["g_depth"] + search_state["s_depth"] - scan_depth

        if scan_depth == 0 or game_state.is_done:
            return [self.score_state(game_state, search_state), None]
        else:
            if game_state.is_maxer:
                max_best = [lb, None]

                for new_state in self.next_states(game_state, search_state):
                    alpha_meta = max_best if max_best[0] > max_prior_best[0] else max_prior_best

                    [next_score, pos] = self.alpha_beta_max(
                        new_state,
                        search_state,
                        scan_depth - 1,
                        alpha_meta,
                        min_prior_best
                    )
                    if next_score > max_best[0]:
                        max_best = [next_score, new_state]

                    if min_prior_best <= max_best:
                        # Avoiding searching (pruning) the rest of the moves and their descendents
                        # because max_best is higher than miner's prior best option. Don't have to look
                        # further if this is the case because on a prior move, miner will prefer
                        # lower alternative
                        set_(search_state, "killers." + str(g_d) + ".miner", min_prior_best)
                        return max_best
                return max_best
            else:
                min_best = [ub, None]

                for new_state in self.next_states(game_state, search_state):
                    beta_meta = min_best if min_best[0] < min_prior_best[0] else min_prior_best

                    [next_score, pos] = self.alpha_beta_max(
                        new_state,
                        search_state,
                        scan_depth - 1,
                        max_prior_best,
                        beta_meta
                    )
                    if next_score < min_best[0]:
                        min_best = [next_score, new_state]

                    if max_prior_best >= min_best:
                        set_(search_state, "killers." + str(g_d) + ".maxer", max_prior_best)
                        return min_best
                return min_best
