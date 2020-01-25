import string

initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

highest_score = 2 ** 16 - 1
lowest_score = -highest_score

white = "w"
black = "b"

color_o = {
    white: black,
    black: white
}

affinity = {
    white: 1,
    black: -1
}

pieces = {
    white: set("RNBQKP"),
    black: set("rnbqkp")
}

all_pieces = pieces[white] | pieces[black]

pawns = set("pP")
knights = set("nN")
bishops = set("bB")
rooks = set("rR")
queens = set("qQ")
kings = set("kK")
major_pieces = knights | bishops | rooks | queens
not_pawns = "NnBbRrQqKk"

pinners = {
    white: set("QRB"),
    black: set("qrb")
}

all_pinners = pinners[white] | pinners[black]

b_range = set(range(0, 8))

# for chess "algebraic notation"
ranks = list(range(8, 0, -1))
files = list(string.ascii_lowercase)[:8]

material = {
    "k": -10000,
    "q": -1100,
    "r": -525,
    "b": -350,
    "n": -350,
    "p": -60,
    "P": 60,
    "N": 350,
    "B": 350,
    "R": 525,
    "Q": 1100,
    "K": 10000,
    None: 0
}

castling = {
    white: "KQ",
    black: "kq"
}

associations = {
    white: (pieces[black], pieces[white]),
    black: (pieces[white], pieces[black])
}

castling_block = {
    "K": [(7, 6), (7, 5)],
    "Q": [(7, 1), (7, 2), (7, 3)],
    "k": [(0, 6), (0, 5)],
    "q": [(0, 1), (0, 2), (0, 3)]
}

castling_check = {
    "K": [(7, 6), (7, 5)],
    "Q": [(7, 2), (7, 3)],
    "k": [(0, 6), (0, 5)],
    "q": [(0, 2), (0, 3)]
}

corners = set([
    (7, 7),
    (7, 0),
    (0, 7),
    (0, 0)
])

castling_rooks = {
    "K": (7, 7),
    "Q": (7, 0),
    "k": (0, 7),
    "q": (0, 0)
}

initial_positions = {
    'p': {(1, 2), (1, 5), (1, 1), (1, 4), (1, 7), (1, 0), (1, 6), (1, 3)},
    'n': {(0, 1), (0, 6)},
    'b': {(0, 2), (0, 5)},
    'r': {(0, 7), (0, 0)},
    'q': {(0, 3)},
    'k': {(0, 4)},
    'P': {(6, 2), (6, 5), (6, 1), (6, 4), (6, 7), (6, 0), (6, 6), (6, 3)},
    'N': {(7, 6), (7, 1)},
    'B': {(7, 5), (7, 2)},
    'R': {(7, 0), (7, 7)},
    'Q': {(7, 3)},
    'K': {(7, 4)}
}
