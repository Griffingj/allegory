from src.search import minimax, alpha_beta_basic, GameSearch


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
