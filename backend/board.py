"""
Module to manage the memory of the chessboard.
"""

import json

import numpy as np


class Piece:
    "Abstract class of chess pieces"

    def legal(self, _bit_pos_start, bit_pos_end, game):
        "Function to know the legalty of a move (outside the board, some pieces already there ...)"
        if bit_pos_end > 63 or bit_pos_end <= 0:
            return False

        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8
        if game.board[line_end][row_end].color == self.color:
            return False
        return True

    def possibilities(self, _bit_pos_start, _game):
        "Function to know the different moves possibles"
        raise NotImplementedError

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.check = False


class Rock(Piece):
    "Class to define the move available for a rock"

    def legal(self, bit_pos_start, bit_pos_end, game):
        if not super().legal(bit_pos_start, bit_pos_end, game):
            return False

        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8

        legal_rock = (line_end == line_start) or (row_end == row_start)

        if not legal_rock:
            return False

        possibilities = self.possibilities(bit_pos_start, game)
        return [line_end, row_end] in possibilities

    def possibilities(self, bit_pos_start, game):
        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8

        max_left_candidates = [0]
        max_right_candidates = [7]
        max_bot_candidates = [0]
        max_top_candidates = [7]

        for case in range(8):
            if game.board[line_start][case] != {}:
                if case < row_start:
                    max_left_candidates.append(case)
                elif case > row_start:
                    max_right_candidates.append(case)

            if game.board[case][row_start] != {}:
                if case < line_start:
                    max_bot_candidates.append(case)
                elif case > line_start:
                    max_top_candidates.append(case)

        max_left = max(max_left_candidates)
        if (
            game.board[line_start][max_left].color == self.color
            and max_left != row_start
        ):
            max_left += 1

        max_right = min(max_right_candidates)
        if (
            game.board[line_start][max_right].color == self.color
            and max_left != row_start
        ):
            max_right -= 1

        max_bot = min(max_bot_candidates)
        if game.board[max_bot][row_start].color == self.color and max_bot != line_start:
            max_bot += 1

        max_top = min(max_top_candidates)
        if game.board[max_top][row_start].color == self.color and max_top != line_start:
            max_top -= 1

        possibilities = []

        for x in range(max_left, max_right):
            possibilities.append([line_start, x])
        for y in range(max_bot, max_top):
            possibilities.append([y, row_start])

        return possibilities


class Knight(Piece):
    "Class to define the move available for a knight"

    def legal(self, bit_pos_start, bit_pos_end, game):
        if not super().legal(bit_pos_start, bit_pos_end, game):
            return False

        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8

        if (line_end == line_start + 1) or (line_end == line_start - 1):
            return (row_end == row_start + 2) or (row_end == row_start - 2)
        elif (row_end == row_start + 1) or (row_end == row_start - 1):
            return (line_end == line_start + 2) or (line_end == line_start - 2)

        return False

    def possibilities(self, bit_pos_start, game):
        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8

        decal_one = [-1, 1]
        decal_two = [-2, 2]
        possibilities = []

        for i in decal_one:
            for j in decal_two:
                possibilities.append([line_start + i, row_start + j])
                possibilities.append([line_start + j, row_start + i])

        possibilities = [case for case in possibilities if all(x >= 0 for x in case)]

        for case in possibilities:
            if game.board[case[0]][case[1]] != {}:
                if game.board[case[0]][case[1]].color == self.color:
                    possibilities.remove(case)
                    break

        return possibilities


class Bishop(Piece):
    "Class to define the move available for a bishop"

    def legal(self, bit_pos_start, bit_pos_end, game):
        if not super().legal(bit_pos_start, bit_pos_end, game):
            return False

        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8

        diag_row = max(row_start, row_end) - min(row_start, row_end)
        diag_line = max(line_start, line_end) - min(line_start, line_end)
        legal_bishop = diag_line == diag_row

        if not legal_bishop:
            return False

        possibilities = self.possibilities(bit_pos_start, game)
        return [line_end, row_end] in possibilities

    def possibilities(self, bit_pos_start, game):
        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8

        found_left_bot = False
        found_right_bot = False
        found_left_top = False
        found_right_top = False
        max_left_bot = [0, 0]
        max_right_bot = [0, 7]
        max_left_top = [7, 0]
        max_right_top = [7, 7]

        for case in range(1, 7):
            if not found_left_bot:
                if line_start - case > 0 and row_start - case > 0:
                    if game.board[line_start - case][row_start - case] != {}:
                        max_left_bot[0], max_left_bot[1] = (
                            line_start - case,
                            row_start - case,
                        )
                        found_left_bot = True
                elif row_start - case == 0 and line_start - case == 0:
                    found_left_bot = True
                elif row_start - case == 0:
                    max_left_bot[0], max_left_bot[1] = line_start - case, 0
                    found_left_bot = True
                elif line_start - case == 0:
                    max_left_bot[0], max_left_bot[1] = 0, row_start - case
                    found_left_bot = True

            if not found_right_bot:
                if game.board[line_start - case][row_start + case] != {}:
                    max_right_bot[0], max_right_bot[1] = (
                        line_start - case,
                        row_start + case,
                    )
                    found_right_bot = True
                elif row_start + case == 7 and line_start - case == 0:
                    found_right_bot = True
                elif row_start + case == 7:
                    max_right_bot[0], max_right_bot[1] = line_start - case, 7
                    found_right_bot = True
                elif line_start - case == 0:
                    max_right_bot[0], max_right_bot[1] = 0, row_start - case
                    found_right_bot = True

            if not found_left_top:
                if game.board[line_start + case][row_start - case] != {}:
                    max_left_top[0], max_left_top[1] = (
                        line_start + case,
                        row_start - case,
                    )
                    found_left_top = True
                elif row_start - case == 0 and line_start + case == 7:
                    found_left_top = True
                elif row_start - case == 0:
                    max_left_top[0], max_left_top[1] = line_start + case, 0
                    found_left_top = True
                elif line_start + case == 7:
                    max_left_top[0], max_left_top[1] = 7, row_start - case
                    found_left_top = True

            if not found_right_top:
                if game.board[line_start + case][row_start + case] != {}:
                    max_right_top[0], max_right_top[1] = (
                        line_start + case,
                        row_start + case,
                    )
                    found_right_top = True
                elif row_start + case == 7 and line_start + case == 7:
                    found_right_top = True
                elif row_start + case == 7:
                    max_right_top[0], max_right_top[1] = line_start + case, 7
                    found_right_top = True
                elif line_start + case == 7:
                    max_right_top[0], max_right_top[1] = 7, row_start + case
                    found_right_top = True

        if game.board[max_left_bot[0]][max_left_bot[1]] != {}:
            if game.board[max_left_bot[0]][max_left_bot[1]].color == self.color:
                max_left_bot[0] += 1
                max_left_bot[1] += 1
        if game.board[max_right_bot[0]][max_right_bot[1]] != {}:
            if game.board[max_right_bot[0]][max_right_bot[1]].color == self.color:
                max_right_bot[0] += 1
                max_right_bot[1] -= 1
        if game.board[max_left_top[0]][max_left_top[1]] != {}:
            if game.board[max_left_top[0]][max_left_top[1]].color == self.color:
                max_left_top[0] -= 1
                max_left_top[1] += 1
        if game.board[max_right_top[0]][max_right_top[1]] != {}:
            if game.board[max_right_top[0]][max_right_top[1]].color == self.color:
                max_right_top[0] -= 1
                max_right_top[1] -= 1

        x, y = max_left_bot[0], max_left_bot[1]

        possibilities = []
        while x != max_right_top[0] and y != max_right_top[1]:
            possibilities.append([x, y])
            x += 1
            y += 1

        i, j = max_right_bot[0], max_right_bot[1]
        while i != max_left_top[0] and j != max_left_top[1]:
            possibilities.append([i, j])
            i += 1
            j += 1
        possibilities = [case for case in possibilities if all(x >= 0 for x in case)]
        return possibilities


class Pawn(Piece):
    "Class to define moves available for a pawn"

    def __init__(self, color, name, first_move):
        super().__init__(color, name)
        self.first_move = first_move

    def legal(self, bit_pos_start, bit_pos_end, game):
        if not super().legal(bit_pos_start, bit_pos_end, game):
            return False

        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8

        possibilies = self.possibilities(bit_pos_start, game)
        return [line_end, row_end] in possibilies

    def possibilities(self, bit_pos_start, game):
        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        possibilities = []

        if game.board[line_start][row_start].color == "white":
            if row_start != 0 and game.board[line_start + 1][row_start - 1] != {}:
                possibilities.append([line_start + 1, row_start - 1])
            if row_start != 7 and game.board[line_start + 1][row_start + 1] != {}:
                possibilities.append([line_start + 1, row_start + 1])
            if self.first_move:
                if game.board[line_start + 1][row_start] == {}:
                    possibilities.append([line_start + 1, row_start])
                    if game.board[line_start + 2][row_start] == {}:
                        possibilities.append([line_start + 2, row_start])
            if game.board[line_start + 1][row_start] == {}:
                possibilities.append([line_start + 1, row_start])

        if game.board[line_start][row_start].color == "black":
            if row_start - 1 >= 0 and game.board[line_start - 1][row_start - 1] != {}:
                possibilities.append([line_start - 1, row_start - 1])
            if row_start + 1 < 8 and game.board[line_start - 1][row_start + 1] != {}:
                possibilities.append([line_start - 1, row_start + 1])
            if self.first_move:
                if game.board[line_start - 1][row_start] == {}:
                    possibilities.append([line_start - 1, row_start])
                    if game.board[line_start - 2][row_start] == {}:
                        possibilities.append([line_start - 2, row_start])
            if game.board[line_start - 1][row_start] == {}:
                possibilities.append([line_start - 1, row_start])

        return possibilities


class Queen(Bishop, Rock):
    "Class to define the move available for a Queen"

    def legal(self, bit_pos_start, bit_pos_end, game):
        return Bishop.legal(self, bit_pos_start, bit_pos_end, game) or Rock.legal(
            self, bit_pos_start, bit_pos_end, game
        )

    def possibilities(self, bit_pos_start, game):
        return Bishop.possibilities(self, bit_pos_start, game) + Rock.possibilities(
            self, bit_pos_start, game
        )


class King(Piece):
    "Class to define the move available for a Queen"

    def legal(self, bit_pos_start, bit_pos_end, game):
        if not super().legal(bit_pos_start, bit_pos_end, game):
            return False
        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8

        possibilies = self.possibilities(bit_pos_start, game)
        return [line_end, row_end] in possibilies

    def threats(self, bit_pos_start, game):
        "Function to know if the king is under threat"
        for i in range(8):
            for j in range(8):
                if game.board[i][j].possibilities(bit_pos_start, game):
                    return True
        return False

    def possibilities(self, bit_pos_start, _game):
        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        possibilities = []

        for i in [-1, 1]:
            for j in [-1, 1]:
                if not (line_start + i < 0 or row_start + j < 0):
                    possibilities.append([line_start + i, row_start + j])
            possibilities.append([line_start, row_start + i])
            possibilities.append([line_start + i, row_start])
        return possibilities


class Board:
    """
    The class who manages the memory of a chess board
    """

    def __init__(self) -> None:
        """
        bits_string: the state of the board send by the board in a String of bits
        """
        rock_white = Rock("white", "rockWhite")
        knight_white = Knight("white", "knightWhite")
        bishop_white = Bishop("white", "bishopWhite")
        queen_white = Queen("white", "queenWhite")
        king_white = King("white", "kingWhite")
        pawn_white = Pawn("white", "pawnWhite", True)
        rock_black = Rock("black", "rockBlack")
        knight_black = Knight("black", "knightBlack")
        bishop_black = Bishop("black", "bishopBlack")
        queen_black = Queen("black", "queenBlack")
        king_black = King("black", "kingBlack")
        pawn_black = Pawn("black", "pawnBlack", True)
        empty = {}
        self.board = [
            [
                rock_white,
                knight_white,
                bishop_white,
                queen_white,
                king_white,
                bishop_white,
                knight_white,
                rock_white,
            ],
            [
                pawn_white,
                pawn_white,
                pawn_white,
                pawn_white,
                pawn_white,
                pawn_white,
                empty,
                empty,
            ],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [
                empty,
                empty,
                empty,
                empty,
                empty,
                empty,
                pawn_white,
                pawn_white,
            ],
            [
                pawn_black,
                pawn_black,
                pawn_black,
                pawn_black,
                pawn_black,
                pawn_black,
                pawn_black,
                pawn_black,
            ],
            [
                rock_black,
                knight_black,
                bishop_black,
                queen_black,
                king_black,
                bishop_black,
                knight_black,
                rock_black,
            ],
        ]
        self.move_count = 0
        self.king_white = [0, 4]
        self.king_black = [7, 4]
        self.piece_moved = None

    def state_board(self) -> list:
        """
        Return the state of the board
        """
        return self.board

    def move(self, bit_pos_start, bit_pos_end) -> None:
        """
        Update the board
        """
        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8

        if self.move_count % 2 == 0:
            assert self.board[line_start][row_start].color == "white"
        else:
            assert self.board[bit_pos_start]["color"] == "black"
        if self.legal(bit_pos_start, bit_pos_end, self.board[line_start][row_start]):
            piece = self.board[line_start][row_start]
            self.board[line_start][row_start] = {}
            self.board[line_end][row_end] = piece
            if piece.type() == Pawn:
                piece.first_move = False
            elif piece.type() == King:
                if piece.color == "white":
                    self.king_white = [line_end, row_end]
                else:
                    self.king_black = [line_end, row_end]
        self.move_count += 1

    def legal(self, bit_pos_start, bit_pos_end, piece) -> bool:
        """
        Verifying the legalty of a move
        """

        line_start = bit_pos_start // 8
        row_start = bit_pos_start % 8
        line_end = bit_pos_end // 8
        row_end = bit_pos_end % 8
        game_tmp = self
        game_tmp.board[line_start][row_start] = {}
        game_tmp.board[line_end][row_end] = piece

        if piece.legal(bit_pos_start, bit_pos_end, self):
            if self.move_count % 2 == 0:
                # Check if there is no check
                if self.board[self.king_white[0]][self.king_white[1]].threats(
                    bit_pos_start, self
                ):
                    if game_tmp.board[self.king_white[0]][self.king_white[1]].threats(
                        bit_pos_start, self
                    ):
                        return False
                # Check if the king wont be in check after the move
                if game_tmp.board[self.king_white[0]][self.king_white[1]].threats(
                    bit_pos_start, game_tmp
                ):
                    return False
            else:
                if self.board[self.king_black[0]][self.king_black[1]].threats(
                    bit_pos_start, self
                ):
                    if game_tmp.board[self.king_black[0]][self.king_black[1]].threats(
                        bit_pos_start, self
                    ):
                        return False
                if game_tmp.board[self.king_black[0]][self.king_black[1]].threats(
                    bit_pos_start, game_tmp
                ):
                    return False

    def board_to_bits(self):
        bits = ""
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != {}:
                    bits += "0"
                else:
                    bits += "1"
        return bits

    def update(self, bits_string):
        state = self.board_to_bits()
        if bits_string != state:
            for i in range(64):
                if bits_string[i] != state[i]:
                    if bits_string[i] == "1":
                        if self.piece_moved is not None:
                            self.piece_moved = self.board[i // 8][i % 8]
                        self.board[i // 8][i % 8] = {}
                    if bits_string[i] == "0":
                        self.board[i // 8][i % 8] = self.piece_moved
                        self.piece_moved = None


if __name__ == "__main__":
    game_test = Board()
    # for i in range (8):
    #     for j in range(8):
    #         print(f"({i}, {j})")
    #         if game_test.board[i][j] != {}:
    #             print(game_test.board[i][j].possibilities(i*8+j, game_test))
    with open("data.json") as f:
        board_state = json.load(f)
    state_board_prev = board_state
    array_prev = np.array(list(state_board_prev))
    while True:
        with open("data.json") as f:
            board_state = json.load(f)
        state_board = board_state
        array_now = np.array(list(state_board))
        if state_board != state_board_prev:
            bit_pos_start = np.where(array_prev != array_now)[0]
            state_board_prev = state_board
            array_prev = array_now
            with open("data.json") as f:
                board_state = json.load(f)
            state_board = board_state
            while state_board == state_board_prev:
                with open("data.json") as f:
                    board_state = json.load(f)
                state_board = board_state
            array_now = np.array(list(state_board))
            bit_pos_end = np.where(array_prev != array_now)[0]
            game_test.move(bit_pos_start, bit_pos_end)
        state_board_prev = state_board
