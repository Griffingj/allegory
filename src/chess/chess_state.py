from collections import namedtuple

from src.chess.chess_movement import is_attacked

from src.chess.chess_consts import b_range, white, black, castling_rooks, material, kings, pieces,\
    initial_fen


Undo = namedtuple("Undo", [
    "done",
    "from_",
    "to_",
    "victim",
    "en_passant_target",
    "castling_available",
    "castled_to"
], defaults=(None, None, None, None, None, None))


class ChessState():
    # all 2d coords are in (y, x) form where positive y is down, this is to ease working with 2d array
    # board representation
    def __init__(
            self,
            is_done,  # If the game is in a complete state or not
            active_color,  # Which color (player) whose turn should be played next
            castling_available,  # A str containing all available castling moves, fen style
            en_passant_target,  # If the opponent played a pawn "leap", the coords of that target
            halfmoves,  # TODO The halfmove counter for 50-move stalemate rule
            move,  # The turn counter, incremented after each player has played a turn
            board,
            material_balance,
            king_pos,
            check_state,
            undo_stack):

        self.is_done = is_done
        self.active_color = active_color
        self.castling_available = castling_available
        self.en_passant_target = en_passant_target
        self.halfmoves = halfmoves  # TODO implement later
        self.move = move
        self.board = board
        self.material_balance = material_balance
        self.king_pos = king_pos,
        self.check_state = check_state,
        self.undo_stack = undo_stack
        # self.mobility = mobility

    def to_fen(self):
        # A FEN "record" defines a particular game position, all in one text line and using only the ASCII character
        # set.
        files = []

        for i in b_range:
            empty_c = 0
            file_str = ""

            for j in b_range:
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

    def is_maxer(self):
        return self.active_color == white

    # self.is_done = is_done
    # self.active_color = active_color
    # self.castling_available = castling_available
    # self.en_passant_target = en_passant_target
    # self.halfmoves = halfmoves
    # self.move = move
    # self.board = board
    # self.material_balance = material_balance
    # self.undo_stack = undo_stack

    # Move = namedtuple("Move", [
    #     "from_",
    #     "to_",
    #     "victim",
    #     "en_passant_target",
    #     "castling_available_to",
    #     "castled_to"
    # ], defaults=(None, None, None, None, None, None))

    def board_apply(self, move):
        (f_y, f_x) = move.from_
        (t_y, t_x) = move.to_
        piece = self.board[f_y][f_x]

        self.king_pos[piece] = move.to_

        undo = (
            (piece, move.from_),
            (move.victim, move.to)
        )
        self.board[t_y][t_x] = piece
        self.board[f_y][f_x] = None

        undo_c_rook = None

        if move.castled_to is not None:
            c_from = castling_rooks[move.castled_to]
            c_to = None

            if move.castled_to == "K":
                c_to = (7, 5)
            elif move.castled_to == "Q":
                c_to = (7, 3)
            elif move.castled_to == "k":
                c_to = (0, 5)
            else:
                c_to = (0, 3)

            c_piece = self.board[c_from[0]][c_from[1]]
            self.king_pos[c_piece] = c_to

            undo_c_rook = (
                (c_piece, c_from),
                (None, c_to)
            )
            self.board[c_to[0]][c_to[1]] = c_piece
            self.board[c_from[0]][c_from[1]] = None

        return (undo, undo_c_rook)

    def board_undo(self, back):
        for undos in back:
            for (piece, pos) in undos:
                self.board[pos[0]][pos[1]] = piece

        return self

    def apply(self, move):
        # TODO draw rules halfmove counter etc
        if move.victim is not None:
            self.material_balance -= material[move.victim]

            if move.victim in kings:
                self.done = True

        if move.castling_available_to is not None:
            self.castling_available = move.castling_available_to

        self.en_passant_target = move.en_passant_target

        self.move += 1 if self.active_color == black else 0

        # Color change affects subject in "is_attacked" etc
        self.active_color = black if self.active_color == white else white

        king_piece = "K" if self.active_color == white else "k"
        self.check_state = is_attacked(self, self.king_pos[king_piece])

        return self

    def undo(self, num):
        # TODO
        return self


def calc_material_balance(board):
    balance = 0

    for i in b_range:
        for j in b_range:
            piece = board[i][j]
            if (piece is not None):
                balance += material[piece]

    return balance


def fen_to_state(fen_str):
    [files, color, castling, ept, half_moves, moves] = fen_str.split(" ")
    board = []
    king_pos = dict()
    i = 0

    for file_str in files.split("/"):
        file_arr = []

        for c in file_str:
            if c in pieces:
                file_arr.append(c)

                if c in kings:
                    king_pos[c] = (i, len(file_arr) - 1)
            else:
                for n in range(0, int(c)):
                    file_arr.append(None)
        board.append(file_arr)
        i += 1

    active_king = "K" if color == white else "k"

    state = ChessState(
        is_done=False,
        active_color=color,
        castling_available=castling,
        en_passant_target=ept,
        halfmoves=int(half_moves),
        move=int(moves),
        board=board,
        material_balance=calc_material_balance(board),
        king_pos=king_pos,
        check_state=None,
        undo_stack=[]
    )
    state.check_state = is_attacked(state, king_pos[active_king])

    return state


initial_state = fen_to_state(initial_fen)
