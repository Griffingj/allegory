from search import GameSearch


class Node():
    def __init__(self, static_score, is_maxer, children, is_done=False):
        self.static_score = static_score
        self.is_done = is_done
        self.is_maxer = is_maxer
        self.children = children


def all_valid_moves(g):
    return g.children


game_tree =\
    Node(None, True, [ #7
        Node(1, False, [ # 7
            Node(None, True, [ # 7
                Node(None, False, [# 7
                    Node(8, True, [], True),
                    Node(7, True, [], True)
                ]),
                Node(None, False, [ # 3
                    Node(3, True, [], True),
                    Node(9, True, [], True)
                ])
            ]),
            Node(None, True, [ # 8
                Node(None, False, [ # 8
                    Node(9, True, [], True),
                    Node(8, True, [], True)
                ]),
                Node(None, False, [ # 2
                    Node(2, True, [], True),
                    Node(4, True, [], True)
                ])
            ])
        ])
    ])


def test_minimax():
    score_call_vals = []

    def score_state(g):
        score_call_vals.append(g.static_score)
        return g.static_score

    search = GameSearch(score_state, all_valid_moves)
    search.minimax(game_tree)

    assert score_call_vals == [8, 7, 3, 9, 9, 8, 2, 4]


def test_alpha_beta():
    score_call_vals = []

    def score_state(g):
        score_call_vals.append(g.static_score)
        return g.static_score

    search = GameSearch(score_state, all_valid_moves)
    search.alpha_beta(game_tree)

    assert score_call_vals == [8, 7, 3, 9, 8]


def test_alpha_beta_max():
    score_call_vals = []

    def score_state(g, s):
        score_call_vals.append(g.static_score)
        return g.static_score

    def all_valid_moves(g, s):
        return g.children

    search = GameSearch(score_state, all_valid_moves)
    search_state = {
        "g_depth": 0,
        "s_depth": 5
    }
    result = search.alpha_beta_max(game_tree, search_state, 5)

    assert result[0] == 7
    assert result[1].static_score == 1
    assert score_call_vals == [8, 7, 3, 9, 8]
