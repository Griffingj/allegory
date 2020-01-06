from collections import namedtuple

from src.chess.chess_movement import is_attacked

from src.chess.chess_consts import b_range, white, black, castling_rooks, material, pieces,\
    initial_fen, ranks, files

empty_set = set()

Undo = namedtuple("Undo", [
    "undo_balance",
    "undo_ca",
    "undo_ept",
    "undo_board",
    "undo_check_state",
    "redo_move"
])


def coords_to_chess(pos):
    (y, x) = pos
    return f"{files[x]}{ranks[y]}"


def chess_to_coords(chess):
    [f, r] = list(chess)
    return (ranks.index(int(r)), files.index(f))


class ChessState():
    # all 2d coords are in (y, x) form where positive y is down (from white's perspective),
    # this is to ease working with 2d array board representation
    # e.g. (0, 0) -> a8; (0, 7) -> h8; (7, 0) -> a1; (7,7) -> h1
    def __init__(
            self,
            is_done,  # If the game is in a complete state or not
            active_color,  # Which color (player) whose turn should be played next
            castling_available,  # A str containing all available castling moves, fen style
            en_passant_target,  # If the opponent played a pawn "leap", the coords of that target
            halfmoves,  # TODO The halfmove counter for 50-move stalemate rule
            move,  # The turn counter, incremented after each player has played a turn
            board,
            positions,
            material_balance,
            check_state):

        self.is_done = is_done
        self.active_color = active_color
        self.castling_available = castling_available
        self.en_passant_target = en_passant_target
        self.halfmoves = halfmoves  # TODO implement later
        self.move = move
        self.board = board
        self.positions = positions
        self.material_balance = material_balance
        self.check_state = check_state

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
                    file_str += piece if empty_c == 0 else str(empty_c) + piece
                    empty_c = 0

            if empty_c != 0:
                file_str += str(empty_c)

            files.append(file_str)

        return " ".join([
            "/".join(files),
            self.active_color,
            self.castling_available if self.castling_available is not None else "-",
            coords_to_chess(self.en_passant_target) if self.en_passant_target is not None else "-",
            str(self.halfmoves),
            str(self.move)
        ])

    def is_maxer(self):
        return self.active_color == white

    def board_apply(self, move):
        (f_y, f_x) = move.from_
        (t_y, t_x) = move.to_
        piece = self.board[f_y][f_x]

        undos = [
            (move.from_, move.to_, piece),
            (move.to_, None, move.victim),
        ]

        self.positions[piece].discard(move.from_)
        self.positions[piece].add(move.to_)

        if move.victim is not None:
            self.positions[move.victim].discard(move.to_)

        self.board[t_y][t_x] = piece
        self.board[f_y][f_x] = None

        if move.ept_cap is not None:
            (ept, epp) = move.ept_cap
            (y, x) = ept
            self.positions[epp].discard(ept)
            self.board[y][x] = None
            undos.append((ept, None, epp))

        if move.castle is not None:
            # Have to move the rook too
            c_from = castling_rooks[move.castle]
            c_to = None

            if move.castle == "K":
                c_to = (7, 5)
            elif move.castle == "Q":
                c_to = (7, 3)
            elif move.castle == "k":
                c_to = (0, 5)
            else:
                c_to = (0, 3)

            c_piece = self.board[c_from[0]][c_from[1]]

            undos.append((c_from, c_to, c_piece))
            undos.append((c_to, None, None))
            self.positions[c_piece].discard(c_from)
            self.positions[c_piece].add(c_to)
            self.board[c_to[0]][c_to[1]] = c_piece
            self.board[c_from[0]][c_from[1]] = None

        return undos

    def board_undo(self, undos):
        for undo in undos:
            (from_, to, piece) = undo
            (f_y, f_x) = from_
            self.board[f_y][f_x] = piece

            if piece is not None:
                self.positions[piece].add(from_)

                if to is not None:
                    self.positions[piece].discard(to)

        return self

    def apply(self, move):
        undo_balance = self.material_balance

        # TODO draw rules halfmove counter etc
        if move.victim is not None:
            self.material_balance -= material[move.victim]

        if move.ept_cap is not None:
            (pos, piece) = move.ept_cap
            self.material_balance -= material[piece]

        undo_ca = self.castling_available

        if move.new_castling_available is not None:
            self.castling_available = None if move.new_castling_available == "-" else move.new_castling_available

        undo_ept = self.en_passant_target
        self.en_passant_target = move.new_en_passant_target
        self.move += 1 if self.active_color == black else 0

        undo_board = self.board_apply(move)

        # Color change affects subject in "is_attacked" etc
        self.active_color = black if self.active_color == white else white

        undo_check_state = self.check_state
        king_piece = "K" if self.active_color == white else "k"
        king_pos, = self.positions[king_piece]

        self.check_state = is_attacked(self, king_pos)

        return Undo(
            undo_balance,
            undo_ca,
            undo_ept,
            undo_board,
            undo_check_state,
            move
        )

    def undo(self, undo):
        (
            undo_balance,
            undo_ca,
            undo_ept,
            undo_board,
            undo_check_state,
            move
        ) = undo

        if undo_balance is not None:
            self.material_balance = undo_balance
        if undo_ca is not None:
            self.castling_available = undo_ca
        if undo_ept is not None:
            self.en_passant_target = undo_ept

        self.check_state = undo_check_state
        self.board_undo(undo_board)
        self.move -= 1 if self.active_color == white else 0
        self.active_color = black if self.active_color == white else white
        return move

    def pos(self, pos):
        (y, x) = pos
        return self.board[y][x]


def calc_material_balance(board):
    balance = 0

    for i in b_range:
        for j in b_range:
            piece = board[i][j]
            if (piece is not None):
                balance += material[piece]

    return balance


def fen_to_state(fen_str):
    [files, color, ca, ept, half_moves, moves] = fen_str.split(" ")
    board = []
    positions = {}
    i = 0

    for file_str in files.split("/"):
        file_arr = []

        for c in file_str:
            if c in pieces:
                file_arr.append(c)
                new_pos = positions.get(c, set())
                new_pos.add((i, len(file_arr) - 1))
                positions[c] = new_pos
            else:
                for n in range(0, int(c)):
                    file_arr.append(None)
        board.append(file_arr)
        i += 1

    active_king = "K" if color == white else "k"
    en_passant_target = chess_to_coords(ept) if ept != "-" else None
    castling_available = ca if ca != "-" else None

    state = ChessState(
        is_done=False,
        active_color=color,
        castling_available=castling_available,
        en_passant_target=en_passant_target,
        halfmoves=int(half_moves),
        move=int(moves),
        board=board,
        positions=positions,
        material_balance=calc_material_balance(board),
        check_state=False
    )

    if active_king in positions:
        king_pos, = positions[active_king]
        state.check_state = is_attacked(state, king_pos)
    else:
        raise Exception(f"Counldn't find active king.")

    return state


initial_state = fen_to_state(initial_fen)
