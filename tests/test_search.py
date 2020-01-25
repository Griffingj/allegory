from src.python.chess.chess_strategy import lowest_score, highest_score


def minimax(game_state, next_actions, score_state, apply_action, search_depth, maxer=True):
    if search_depth == 0 or game_state.is_done:
        return score_state(game_state)
    else:
        scores = [lowest_score if maxer else highest_score]

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
        max_prior_best=(lowest_score, None),
        min_prior_best=(highest_score, None)):

    if scan_depth == 0 or game_state.is_done:
        return (score_state(game_state), None)
    else:
        if game_state.is_maxer:
            max_best = (lowest_score, None)

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
            min_best = (highest_score, None)

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


class Node():
    def __init__(self, static_score, is_maxer, children, is_done=False):
        self.static_score = static_score
        self.is_done = is_done
        self.is_maxer = is_maxer
        self.children = children


def all_valid_moves(g):
    return g.children


game_tree =\
    Node(None, True, [  # 7
        Node(None, False, [  # 7
            Node(None, True, [  # 7
                Node(None, False, [  # 7
                    Node(8, True, [], True),
                    Node(7, True, [], True)
                ]),
                Node(None, False, [  # 3
                    Node(3, True, [], True),
                    Node(9, True, [], True)
                ])
            ]),
            Node(None, True, [  # 8
                Node(None, False, [  # 8
                    Node(9, True, [], True),
                    Node(8, True, [], True)
                ]),
                Node(None, False, [  # 2
                    Node(2, True, [], True),
                    Node(4, True, [], True)
                ])
            ])
        ])
    ])


def next_actions(game_state):
    count = len(game_state.children)
    return range(0, count) if count > 0 else []


def apply_action(game_state, action):
    return (game_state.children[action], None)


def score_end(game_state):
    return game_state.static_score


def test_minimax():
    score_call_vals = []

    def score_state(game_state):
        score_call_vals.append(game_state.static_score)
        return game_state.static_score

    minimax(game_tree, next_actions, score_state, apply_action, 5)
    assert score_call_vals == [8, 7, 3, 9, 9, 8, 2, 4]


def test_alpha_beta_basic():
    score_call_vals = []

    def score_state(game_state):
        score_call_vals.append(game_state.static_score)
        return game_state.static_score

    result = alpha_beta_basic(game_tree, next_actions, score_state, apply_action, 5)

    assert result[0] == 7
    assert result[1] == 0
    assert score_call_vals == [8, 7, 3, 9, 8]
