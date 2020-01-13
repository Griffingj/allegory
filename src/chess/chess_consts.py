import string

initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

white = "w"
black = "b"

white_pieces = set("RNBQKP")
black_pieces = set("rnbqkp")
pieces = white_pieces.union(black_pieces)

pawns = set("pP")
knights = set("nN")
bishops = set("bB")
rooks = set("rR")
queens = set("qQ")
kings = set("kK")
major_pieces = knights | bishops | rooks | queens
not_pawns = major_pieces | kings

white_pinners = set("QRB")
black_pinners = set("qrb")
pinners = white_pinners | black_pinners

# bounds checking for coords
b_range = set(range(0, 8))

# for chess "algebraic notation"
ranks = list(range(8, 0, -1))
files = list(string.ascii_lowercase)[:8]

material = {
    "k": -10000,
    "q": -1000,
    "r": -525,
    "b": -350,
    "n": -350,
    "p": -100,
    "P": 100,
    "N": 350,
    "B": 350,
    "R": 525,
    "Q": 1000,
    "K": 10000,
    None: 0
}

white_castling = "KQ"
black_castling = "kq"

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

castling_rooks = {
    "K": (7, 7),
    "Q": (7, 0),
    "k": (0, 7),
    "q": (0, 0)
}
