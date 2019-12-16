import os

pieces = set("rnbqkpRNBQKP")
initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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
    "K": 10000
}


def calc_material_balance(board):
    balance = 0

    for i in range(0, 8):
        for j in range(0, 8):
            piece = board[i][j]
            if (piece is not None):
                balance += material[piece]

    return balance


class ChessState():
    def __init__(
            self,
            is_done,
            active_color,
            castling_available,
            en_passant_target,
            halfmoves,
            move,
            board,
            material_balance):

        self.is_done = is_done
        self.active_color = active_color
        self.castling_available = castling_available
        self.en_passant_target = en_passant_target
        self.halfmoves = halfmoves
        self.move = move
        self.board = board
        self.material_balance = material_balance

    # A FEN "record" defines a particular game position, all in one text line and using only the ASCII character set.
    # A text file with only FEN data records should have the file extension ".fen".[1]

    # A FEN record contains six fields. The separator between fields is a space. The fields are:

    # Piece placement (from White's perspective).
    # Each rank is described, starting with rank 8 and ending with rank 1;
    # within each rank, the contents of each square are described from file "a" through file "h". Following the
    # Standard Algebraic Notation (SAN), each piece is identified by a single letter taken from the standard English
    # names (pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q" and king = "K").[1] White pieces are
    # designated using upper-case letters ("PNBRQK") while black pieces use lowercase ("pnbrqk"). Empty squares are
    # noted using digits 1 through 8 (the number of empty squares), and "/" separates ranks.

    # Active color.
    # "w" means White moves next, "b" means Black moves next.

    # Castling availability.
    # If neither side can castle, this is "-". Otherwise, this has one or more letters: "K" (White can castle kingside),
    # "Q" (White can castle queenside), "k" (Black can castle kingside), and/or "q" (Black can castle queenside).

    # En passant target square in algebraic notation.
    # If there's no en passant target square, this is "-". If a pawn has just made a two-square move, this is the
    # position "behind" the pawn. This is recorded regardless of whether there is a pawn in position to make an
    # en passant capture.[2]

    # Halfmove clock:
    # This is the number of halfmoves since the last capture or pawn advance. This is used to determine if a draw can be
    # claimed under the fifty-move rule.

    # Fullmove number:
    # The number of the full move. It starts at 1, and is incremented after Black's move.

    # Examples

    # Here is the FEN for the starting position:

    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    def to_fen(self):
        files = []

        for i in range(0, 8):
            empty_c = 0
            file_str = ""

            for j in range(0, 8):
                piece = self.board[i][j]

                if (piece is None):
                    empty_c += 1
                else:
                    file_str += piece if empty_c == 0 else empty_c + piece
                    empty_c = 0

            if empty_c != 0:
                file_str += str(empty_c)

            files.append(file_str)

        return " ".join([
            "/".join(files),
            self.active_color,
            self.castling_available,
            self.en_passant_target,
            str(self.halfmoves),
            str(self.move)
        ])

    def mut_do_move(self, move):
        return True

    def mut_undo_move(self, move):
        return False

    def is_maxer(self):
        return self.active_color == "w"

    def pretty(self):
        pretty_str = ""
        for i in range(0, 8):
            for j in range(0, 8):
                piece = self.board[i][j]
                pretty_str += f"[{' ' if piece is None else piece}]"
            pretty_str += os.linesep

        return pretty_str


def fen_to_state(fen_str):
    [files, color, castling, ep, half_moves, moves] = fen_str.split(" ")
    board = []

    for file_str in files.split("/"):
        file_arr = []
        for c in file_str:
            if c in pieces:
                file_arr.append(c)
            else:
                for i in range(0, int(c)):
                    file_arr.append(None)
        board.append(file_arr)

    return ChessState(
        is_done=False,
        active_color=color,
        castling_available=castling,
        en_passant_target=ep,
        halfmoves=int(half_moves),
        move=int(moves),
        board=board,
        material_balance=calc_material_balance(board)
    )


initial_state = fen_to_state(initial_fen)


# Enhancements
# Quiescence_Search https://www.chessprogramming.org/Quiescence_Search see https://www.chessprogramming.org/Horizon_Effect
# Transposition Table https://www.chessprogramming.org/Transposition_Table
# Killer Heuristic https://www.chessprogramming.org/Killer_Heuristic
# Last_Best_Reply https://www.chessprogramming.org/Last_Best_Reply
# Static_Exchange_Evaluation https://www.chessprogramming.org/Static_Exchange_Evaluation

def score_state(chess_state, search_state):
    # Enhancements https://www.chessprogramming.org/Evaluation#2015_...
    return chess_state.material_balance

def next_states(chess_state, search_state):
    return True
    # while num < n:
    #     yield num
    #     num += 1
