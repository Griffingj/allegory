import re
from collections import namedtuple

from src.python.chess.chess_consts import b_range, white, black, castling_rooks, material, pieces,\
    initial_fen, kings, pawns, castling, initial_positions, rooks, all_pieces, associations,\
    color_o, affinity

from src.python.primitive import intersect_str, subtract_str, sign

from src.python.chess.chess_interop import coords_to_chess, chess_to_coords

from src.python.vector2 import add, subtract, v2_abs

from src.python.chess.chess_movement import abs_unit_d, left_two, right_two, left_one, right_one

fen_invalid = re.compile(r"[^wba-h0-9pnbrqkPNBRQK\/\- ]")

fen_pattern = re.compile(
    r"^(([1-8pnbrqkPNBRQK]){1,8}\/){7}[1-8pnbrqkPNBRQK]{1,8} [wb] [-KQkq]{1,4} (([a-h][1-8])|-) \d+ \d+$"
)

Undo = namedtuple("Undo", [
    "undo_balance",
    "undo_ca",
    "undo_ept",
    "undo_board",
    "redo_move"
])

top_bottom = set([0, 7])


def normal_ca(ca_):
    return None if ca_ is None or len(ca_) == 0 else ca_


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
            total_material):

        self.is_done = is_done
        self.active_color = active_color
        self.castling_available = castling_available
        self.en_passant_target = en_passant_target
        self.halfmoves = halfmoves  # TODO implement later
        self.move = move
        self.board = board
        self.positions = positions
        self.material_balance = material_balance
        self.total_material = total_material

    def is_losing(self, p_color):
        return abs(self.material_balance) > material["N"] and affinity[p_color] != sign(self.material_balance)

    def to_fen_base(self):
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
            coords_to_chess(self.en_passant_target) if self.en_passant_target is not None else "-"
        ])

    def to_fen(self):
        return self.to_fen_base() + " " + str(self.halfmoves) + " " + str(self.move)

    def player_affinity(self):
        return 1 if self.active_color == white else -1

    def board_apply(self, move, promotion):
        (f_y, f_x) = move.from_
        (t_y, t_x) = move.to_
        piece = self.board[f_y][f_x]

        queen = "Q" if self.active_color == white else "q"
        to_piece = queen if promotion else piece

        undos = [
            (move.from_, move.to_, piece)
        ]

        if promotion:
            undos.append((None, move.to_, queen))

        if move.victim is not None:
            undos.append((move.to_, None, move.victim))

        self.positions[piece].discard(move.from_)
        self.positions[to_piece].add(move.to_)

        if move.victim is not None:
            self.positions[move.victim].discard(move.to_)

        self.board[t_y][t_x] = to_piece
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
            c_to = add(left_one if move.castle in kings else right_one, move.to_)
            c_piece = self.board[c_from[0]][c_from[1]]
            undos.append((c_from, c_to, c_piece))
            self.positions[c_piece].discard(c_from)
            self.positions[c_piece].add(c_to)
            self.board[c_to[0]][c_to[1]] = c_piece
            self.board[c_from[0]][c_from[1]] = None

        return undos

    def board_undo(self, undos):
        for undo in undos:
            (from_, to, piece) = undo

            if from_ is not None:
                (f_y, f_x) = from_
                self.board[f_y][f_x] = piece

                if to is not None:
                    (t_y, t_x) = to
                    # If a victim needs to be replaced there will be a following undo for that
                    self.board[t_y][t_x] = None

                if piece is not None:
                    self.positions[piece].add(from_)
                    self.positions[piece].discard(to)
            else:
                # Promotions and magic moves
                self.board[t_y][t_x] = None
                self.positions[piece].discard(to)

        return self

    def apply(self, move):
        piece_moved = self.pos(move.from_)

        # ==== Castling ====
        undo_ca = self.castling_available
        ca_total = "" if self.castling_available is None else self.castling_available
        ca_color_base = castling[self.active_color]
        ca_color_active = intersect_str(ca_total, ca_color_base)

        if piece_moved in kings:
            if move.from_ in initial_positions[piece_moved]:
                diff = subtract(move.to_, move.from_)
                if diff == left_two or diff == right_two or v2_abs(diff) in abs_unit_d:
                    # Remove all ca for if king moves
                    self.castling_available = normal_ca(subtract_str(ca_total, ca_color_base))
                else:
                    raise AssertionError("Encountered unexpected king move")

        elif piece_moved in rooks:
            for castling_key in ca_color_active:
                if castling_rooks[castling_key] == move.from_:
                    self.castling_available = normal_ca(subtract_str(ca_total, castling_key))
                    break

        # ==== Victim ====

        undo_balance = self.material_balance

        if move.victim is not None:
            self.material_balance -= material[move.victim]

        if move.victim in kings:
            self.is_done = True
        elif move.victim in rooks:
            # Remove castling availability for dead rook if it hasn't moved
            for k in subtract_str(ca_total, castling[self.active_color]):
                if castling_rooks[k] == move.to_:
                    self.castling_available = normal_ca(subtract_str(ca_total, k))

        self.move += 1 if self.active_color == black else 0
        self.halfmoves = self.halfmoves + 1

        # ==== En Passant ====

        if move.ept_cap is not None:
            (pos, piece) = move.ept_cap
            self.material_balance -= material[piece]

        undo_ept = self.en_passant_target
        self.en_passant_target = move.new_ept

        # ==== Movement ====

        promotion = piece_moved in pawns and move.to_[0] in top_bottom

        if promotion:
            self.material_balance += (material["Q"] - material["P"]) * self.player_affinity()

        undo_board = self.board_apply(move, promotion)

        # ==== Done ====

        self.active_color = color_o[self.active_color]

        return Undo(
            undo_balance,
            undo_ca,
            undo_ept,
            undo_board,
            move
        )

    def undo(self, undo):
        (
            undo_balance,
            undo_ca,
            undo_ept,
            undo_board,
            move
        ) = undo

        self.material_balance = undo_balance
        self.castling_available = undo_ca
        self.en_passant_target = undo_ept
        self.board_undo(undo_board)
        self.move -= 1 if self.active_color == white else 0
        self.halfmoves = self.halfmoves - 1
        self.active_color = color_o[self.active_color]
        self.is_done = False
        return move

    def pos(self, pos):
        (y, x) = pos
        return self.board[y][x]

    def format_ascii(self):
        board_str = ""
        for i in b_range:
            rank = "["
            for j in b_range:
                next_ = self.board[i][j]
                rank += "_" if next_ is None else next_
            rank += "]\n"
            board_str += rank
        return board_str

    def hash(self):
        return self.to_fen_base()
        # return tuple((k, tuple(v)) for k, v in self.positions.items())


def normalize_fen(fenish):
    striped = re.sub(r"\s+", " ", fenish.strip())
    return re.sub(fen_invalid, "", striped)


def head(iterable):
    return next(iter(iterable))


def fen_to_state(fen_str, strict=True):
    clean = normalize_fen(fen_str)

    if fen_pattern.search(clean) is None:
        raise Exception(f"Fen bad format, '{fen_str}'")

    [files, active_color, ca, ept, half_moves, moves] = clean.split(" ")
    board = []
    positions = {}
    i = 0
    balance = 0
    total_material = 0

    for p in all_pieces:
        positions[p] = set()

    for file_str in files.split("/"):
        file_arr = []

        for c in file_str:
            if c in all_pieces:
                file_arr.append(c)
                balance += material[c]
                total_material += abs(material[c])
                positions.get(c).add((i, len(file_arr) - 1))
            else:
                for n in range(0, int(c)):
                    file_arr.append(None)
        board.append(file_arr)
        i += 1

    if strict:
        for color in (white, black):
            king = head((kings & pieces[color]))
            if not len(positions[king]):
                raise Exception(f"No {color} king present in fen")

        if ca != "-":
            for color in (white, black):
                color_ca = intersect_str(castling[color], ca)
                king = head((kings & pieces[color]))

                if len(color_ca) and head(initial_positions[king]) not in positions[king]:
                    raise Exception(f"Found unexpected castling availability when {color} King already moved")

                rook = head((rooks & pieces[color]))
                for k in color_ca:
                    (y, x) = castling_rooks[k]
                    if board[y][x] != rook:
                        raise Exception(f"Found unexpected castling availability when {color} Rook already moved")

        if ept != "-":
            offset = (1, 0)
            expected_rank = 3

            if active_color == black:
                offset = (-1, 0)
                expected_rank = 4

            (y, x) = add(chess_to_coords(ept), offset)

            if y != expected_rank:
                raise Exception(f"Unexpected en passant target rank '{y}'")

            p = board[y][x]
            (enemies, _) = associations[active_color]

            if p is None or p not in pawns or p not in enemies:
                raise Exception("En passant target is not found in board")

    en_passant_target = chess_to_coords(ept) if ept != "-" else None
    castling_available = ca if ca != "-" else None

    state = ChessState(
        is_done=False,
        active_color=active_color,
        castling_available=castling_available,
        en_passant_target=en_passant_target,
        halfmoves=int(half_moves),
        move=int(moves),
        board=board,
        positions=positions,
        material_balance=balance,
        total_material=total_material
    )
    return state


initial_state = fen_to_state(initial_fen)
