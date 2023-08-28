"""
This module contains the classes and functions necessary to play a game of
checkers.

Classes:
    PieceColor : Enum : An enum representing the color of a piece.
    Piece : Class : A class representing a piece in a game of checkers.
    Board : Class : A class representing a game board.
    Checkers : Class : A class representing a game of checkers.

Examples:
    board = Checkers() # Creates a new game of checkers
    board.get_whose_turn() -> "BLACK" # Gets whose turn it is, either "RED" or "BLACK"
    b.move_piece((5, 0), (4, 1)) # Moves a piece
    board.get_whose_turn() -> "RED" # Now it is the red player's turn
    board.move_piece((2, 1), (3, 0)) # Moves a piece
    board.get_valid_player_moves("BLACK") -> {
        (6, 1): [(5, 0)],
        (5, 4): [(4, 5), (4, 3)],
        (5, 6): [(4, 7), (4, 5)],
        (4, 1): [(3, 2)],
        (5, 2): [(4, 3)]
    } # Gets all valid moves for a player
    board.is_game_over() -> False # Checks if the game is over
    board.get_winner() -> None # Gets the winner of the game
"""

from __future__ import annotations
from typing import Optional
from enum import Enum


PieceColor = Enum("PieceColor", ["RED", "BLACK"])
"""
Enum type for representing the color of a piece.
"""


class Piece:
    """
    Class representing a piece in a game of checkers.
    """

    def __init__(
        self, color: PieceColor, coordinates: tuple[int, int], is_king: bool = False
    ) -> None:
        """
        Constructor for a Piece object.

        Parameters:
            color : PieceColor : The color of the piece.
            row : int : The row of the piece on the board.
            column : int : The column of the piece on the board.
            is_king : bool : Whether or not the piece is a king.
        """
        self._color = color
        row, column = coordinates
        self._row = row
        self._column = column
        self._is_king = is_king

    def get_color(self) -> str:
        """
        Get a piece's color.

        Returns:
            str : The piece's color
        """
        if self._color == PieceColor.RED:
            return "RED"
        return "BLACK"

    def get_coordinates(self) -> tuple[int, int]:
        """
        Get a piece's coordinates.

        Returns:
            tuple[int, int] : The piece's coordinates
        """
        return (self._row, self._column)

    def set_coordinates(self, coordinates: tuple[int, int]) -> None:
        """
        Set a piece's coordinates.

        Parameters:
            row : int : The piece's new row
            column : int : The piece's new column
        """
        row, column = coordinates
        self._row = row
        self._column = column

    def is_king(self) -> bool:
        """
        Check if a piece is a king.

        Returns:
            bool : Whether or not the piece is a king
        """
        return self._is_king

    def _set_to_king(self) -> None:
        """
        Set a piece to a king.
        """
        self._is_king = True


class Board:
    def __init__(self, rows: int, columns: int) -> None:
        """
        Constructor for a board with no pieces.

        Parameters:
            rows : int : The number of rows on the board
            columns : int : The number of columns on the board
        """
        self._rows = rows
        self._columns = columns
        self._board = [[None for _ in range(self._columns)]
                       for _ in range(self._rows)]

    def _get_square(self, coordinates: tuple[int, int]) -> Optional[Piece]:
        """
        Returns what is in a square on the board.

        Parameters:
            coordinates : tuple[int, int] : The coordinates of the square

        Returns:
            Optional[Piece] : The piece in the square or None if the square is empty
        """
        if not self._is_valid_square(coordinates):
            raise ValueError("Invalid square")
        row, column = coordinates
        return self._board[row][column]

    def _set_square(self, coordinates: tuple[int, int], piece: Optional[Piece]) -> None:
        """
        Set a square on the board to a piece.

        Parameters:
            coordinates : tuple[int, int] : The coordinates of the square
            piece : Piece : The piece to set the square to

        Raises:
            ValueError : If the coordinates are invalid
        """
        if not self._is_valid_square(coordinates):
            raise ValueError("Invalid square")
        row, column = coordinates
        self._board[row][column] = piece

    def _is_valid_square(self, coordinates: tuple[int, int]) -> bool:
        """
        Checks if a square exists on the board.

        Parameters:
            coordinates : tuple[int, int] : The coordinates of the square

        Returns:
            bool : Whether or not the square exists on the board
        """
        row, column = coordinates
        return 0 <= row < self._rows and 0 <= column < self._columns


class Checkers:
    def __init__(self, n: int = 3) -> None:
        """
        Constructor for a game of checkers.

        Parameters:
            n : int : The rows of pieces on each side of the board
        """
        self._rows = 2 * n + 2
        self._columns = 2 * n + 2
        self._board = Board(self._rows, self._columns)
        self._red_player_pieces = set()
        self._black_player_pieces = set()
        self._add_pieces()
        self._whose_turn = "BLACK"

    def _add_pieces(self):
        """
        Adds pieces to the board for the start of a checkers game.
        """
        for row in range(self._board._rows):
            for column in range(self._board._columns):
                coordinates = (row, column)
                if row % 2 != column % 2:
                    if row < self._board._rows // 2 - 1:
                        piece = Piece(PieceColor.RED, coordinates)
                        self._board._set_square(coordinates, piece)
                        self._red_player_pieces.add(coordinates)
                    elif row > self._board._rows // 2:
                        piece = Piece(PieceColor.BLACK, coordinates)
                        self._board._set_square(coordinates, piece)
                        self._black_player_pieces.add(coordinates)

    def get_whose_turn(self):
        return self._whose_turn

    def __str__(self) -> str:
        """
        Returns a string representation of the checkers board.

        Returns: str : A string representation of the board.
        """
        board_string = []
        for row in self._board._board:
            cur = []
            for cell in row:
                if cell is not None:
                    if cell.get_color() == "RED":
                        cur.append("R")
                    else:
                        cur.append("B")
                else:
                    cur.append("_")
            board_string.append(" ".join(cur))
        return "\n".join(board_string) + f"\nPlayer turn: {self.get_whose_turn()}"

    def _is_valid_square(self, coordinates: tuple[int, int]) -> bool:
        """
        Returns whether a square is valid.

        Parameters:
            coordinates : tuple[int, int] : The coordinates of the square.

        Returns: bool : Whether the square is valid.
        """
        row, column = coordinates
        return row >= 0 and row < self._rows and column >= 0 and column < self._columns

    def get_square(self, coordinates: tuple[int, int]) -> Optional[Piece]:
        """
        Checks if a square on the board is occupied and returns the piece
        occupying it if it is.

        Parameters:
            coordinates : tuple[int, int] : The coordinates of the square to
            check.

        Returns: Optional[Piece] : The piece occupying the square, or None if
        the square is empty.
        """
        if not self._board._is_valid_square(coordinates):
            raise ValueError("Invalid square")
        return self._board._get_square(coordinates)

    def get_valid_piece_moves(self, piece_coordinates: tuple) -> list[tuple[int, int]]:
        """
        Returns a list of valid moves for a piece.

        Parameters:
            piece_coordinates : tuple[int, int] : The coordinates of the piece
            to be moved.

        Returns: list[tuple[int, int]] : A list of valid moves for the piece.
        """
        piece = self._board._get_square(piece_coordinates)
        if piece is None:
            return []
        row, column = piece_coordinates
        moves = []
        if piece.get_color() == "RED":
            if (
                self._is_valid_square((row + 1, column + 1))
                and self.get_square((row + 1, column + 1)) is None
            ):
                moves.append((row + 1, column + 1))
            elif (
                self._is_valid_square((row + 2, column + 2))
                and self.get_square((row + 2, column + 2)) is None
                and self.get_square((row + 1, column + 1)) is not None
                and self.get_square((row + 1, column + 1)).get_color() == "BLACK"
            ):
                moves.append((row + 2, column + 2))
            if (
                self._is_valid_square((row + 1, column - 1))
                and self._board._get_square((row + 1, column - 1)) is None
            ):
                moves.append((row + 1, column - 1))
            elif (
                self._is_valid_square((row + 2, column - 2))
                and self._board._get_square((row + 2, column - 2)) is None
                and self._board._get_square((row + 1, column - 1)) is not None
                and self._board._get_square((row + 1, column - 1)).get_color()
                == "BLACK"
            ):
                moves.append((row + 2, column - 2))
            if piece.is_king():
                if (
                    self._is_valid_square((row - 1, column + 1))
                    and self._board._get_square((row - 1, column + 1)) is None
                ):
                    moves.append((row - 1, column + 1))
                elif (
                    self._is_valid_square((row - 2, column + 2))
                    and self._board._get_square((row - 2, column + 2)) is None
                    and self._board._get_square((row - 1, column + 1)) is not None
                    and self._board._get_square((row - 1, column + 1)).get_color()
                    == "BLACK"
                ):
                    moves.append((row - 2, column + 2))
                if (
                    self._is_valid_square((row - 1, column - 1))
                    and self._board._get_square((row - 1, column - 1)) is None
                ):
                    moves.append((row - 1, column - 1))
                elif (
                    self._is_valid_square((row - 2, column - 2))
                    and self._board._get_square((row - 2, column - 2)) is None
                    and self._board._get_square((row - 1, column - 1)) is not None
                    and self._board._get_square((row - 1, column - 1)).get_color()
                    == "BLACK"
                ):
                    moves.append((row - 2, column - 2))
        else:
            if (
                self._is_valid_square((row - 1, column + 1))
                and self._board._get_square((row - 1, column + 1)) is None
            ):
                moves.append((row - 1, column + 1))
            elif (
                self._is_valid_square((row - 2, column + 2))
                and self._board._get_square((row - 2, column + 2)) is None
                and self._board._get_square((row - 1, column + 1)) is not None
                and self._board._get_square((row - 1, column + 1)).get_color() == "RED"
            ):
                moves.append((row - 2, column + 2))
            if (
                self._is_valid_square((row - 1, column - 1))
                and self._board._get_square((row - 1, column - 1)) is None
            ):
                moves.append((row - 1, column - 1))
            elif (
                self._is_valid_square((row - 2, column - 2))
                and self._board._get_square((row - 2, column - 2)) is None
                and self._board._get_square((row - 1, column - 1)) is not None
                and self._board._get_square((row - 1, column - 1)).get_color() == "RED"
            ):
                moves.append((row - 2, column - 2))
            if piece.is_king():
                if (
                    self._is_valid_square((row + 1, column + 1))
                    and self._board._get_square((row + 1, column + 1)) is None
                ):
                    moves.append((row + 1, column + 1))
                elif (
                    self._is_valid_square((row + 2, column + 2))
                    and self._board._get_square((row + 2, column + 2)) is None
                    and self._board._get_square((row + 1, column + 1)) is not None
                    and self._board._get_square((row + 1, column + 1)).get_color()
                    == "RED"
                ):
                    moves.append((row + 2, column + 2))
                if (
                    self._is_valid_square((row + 1, column - 1))
                    and self._board._get_square((row + 1, column - 1)) is None
                ):
                    moves.append((row + 1, column - 1))
                elif (
                    self._is_valid_square((row + 2, column - 2))
                    and self._board._get_square((row + 2, column - 2)) is None
                    and self._board._get_square((row + 1, column - 1)) is not None
                    and self._board._get_square((row + 1, column - 1)).get_color()
                    == "RED"
                ):
                    moves.append((row + 2, column - 2))
        return moves

    def get_jump_moves(
        self, player: str
    ) -> dict[tuple[int, int]: list[tuple[int, int]]]:
        """
        Returns all jump moves for a player.

        Parameters:
            player : str : The color of the player.

        Returns: dict[tuple[int, int] : list[tuple[int, int]]] : A dictionary of
        jump moves for the player.
        """
        if player == "RED":
            player_moves = self.get_all_valid_player_moves("RED")
        else:
            player_moves = self.get_all_valid_player_moves("BLACK")
        jump_moves = {}
        for piece, moves in player_moves.items():
            for move in moves:
                if abs(move[0] - piece[0]) != 1:
                    jump_moves[piece] = jump_moves.get(piece, []) + [move]
        return jump_moves

    def has_jump_move(self, player: str) -> bool:
        """
        Returns whether or not the player has a jump move.

        Parameters:
            player : str : The color of the player.

        Returns: bool : Whether or not the player has a jump move.
        """
        return len(self.get_jump_moves(player)) > 0

    def get_all_valid_player_moves(
        self, color: str
    ) -> dict[tuple[int, int]: list[tuple[int, int]]]:
        """
        Returns all valid moves for a player.

        Parameters:
            color : str : The color of the player.

        Returns: list[list[tuple[int, int]]] : A list of valid moves for the
        player.
        """
        moves = {}
        pieces = (
            self._red_player_pieces if color == "RED" else self._black_player_pieces
        )
        for coordinates in pieces:
            if len(self.get_valid_piece_moves(coordinates)) > 0:
                moves[coordinates] = self.get_valid_piece_moves(coordinates)
        return moves

    def get_valid_player_moves(self, color: str) -> dict[tuple[int, int]: list[tuple[int, int]]]:
        """
        Returns the valid moves a player can actually make.

        Parameters:
            color : str : The color of the player.

        Returns: dict[tuple[int, int] : list[tuple[int, int]]] : A dictionary of
        valid moves for the player.
        """
        if self.has_jump_move(color):
            return self.get_jump_moves(color)
        else:
            return self.get_all_valid_player_moves(color)

    def move_piece(
        self,
        piece_coordinates: tuple[int, int],
        destination_coordinates: tuple[int, int],
    ) -> None:
        """
        Moves a piece from one square to another.

        Parameters:
            piece_coordinates : tuple[int, int] : The coordinates of the piece
            to move.
            destination_coordinates : tuple[int, int] : The coordinates of the
            square to move the piece to.
        """
        piece = self._board._get_square(piece_coordinates)
        kinging_move = False
        if piece is None:
            raise Exception("There is no piece at the given coordinates.")
        if piece.get_color() == "RED":
            # if self._whose_turn != "RED":
            #     raise Exception("It is not red's turn.")
            if destination_coordinates not in self.get_valid_piece_moves(
                piece_coordinates
            ):
                raise Exception(
                    "The piece cannot move to the given coordinates")
            if self.has_jump_move(
                "RED"
            ) and destination_coordinates not in self.get_jump_moves("RED").get(
                piece_coordinates, []
            ):
                raise Exception("The piece must jump if it can.")
            self._board._set_square(piece_coordinates, None)
            self._board._set_square(destination_coordinates, piece)
            self._red_player_pieces.remove(piece_coordinates)
            self._red_player_pieces.add(destination_coordinates)
            piece._row = destination_coordinates[0]
            piece._column = destination_coordinates[1]
            if destination_coordinates[0] == self._board._rows - 1:
                piece._set_to_king()
                kinging_move = True
            if abs(destination_coordinates[0] - piece_coordinates[0]) == 2:
                self._board._set_square(
                    (
                        (destination_coordinates[0] +
                         piece_coordinates[0]) // 2,
                        (destination_coordinates[1] +
                         piece_coordinates[1]) // 2,
                    ),
                    None,
                )
                self._black_player_pieces.remove(
                    (
                        (destination_coordinates[0] +
                         piece_coordinates[0]) // 2,
                        (destination_coordinates[1] +
                         piece_coordinates[1]) // 2,
                    )
                )
            if not self.has_jump_move("RED") or kinging_move:
                self._whose_turn = "BLACK"
        else:
            # if self._whose_turn != "BLACK":
            #     raise Exception("It is not black's turn.")
            if destination_coordinates not in self.get_valid_piece_moves(
                piece_coordinates
            ):
                raise Exception(
                    "The piece cannot move to the given coordinates.")
            if self.has_jump_move(
                "BLACK"
            ) and destination_coordinates not in self.get_jump_moves("BLACK").get(
                piece_coordinates, []
            ):
                raise Exception("The piece must jump if it can.")
            self._board._set_square(piece_coordinates, None)
            self._board._set_square(destination_coordinates, piece)
            self._black_player_pieces.remove(piece_coordinates)
            self._black_player_pieces.add(destination_coordinates)
            piece._row = destination_coordinates[0]
            piece._column = destination_coordinates[1]
            if destination_coordinates[0] == 0:
                piece._set_to_king()
                kinging_move = True
            if abs(destination_coordinates[0] - piece_coordinates[0]) == 2:
                self._board._set_square(
                    (
                        (destination_coordinates[0] +
                         piece_coordinates[0]) // 2,
                        (destination_coordinates[1] +
                         piece_coordinates[1]) // 2,
                    ),
                    None,
                )
                self._red_player_pieces.remove(
                    (
                        (destination_coordinates[0] +
                         piece_coordinates[0]) // 2,
                        (destination_coordinates[1] +
                         piece_coordinates[1]) // 2,
                    )
                )
            if not self.has_jump_move("BLACK") or kinging_move:
                self._whose_turn = "RED"

    def is_game_over(self) -> bool:
        """
        Returns whether or not the game is over.

        Returns: bool : Whether or not the game is over.
        """
        if (
            len(self.get_valid_player_moves("RED")) == 0
            or len(self.get_valid_player_moves("BLACK")) == 0
        ):
            return True
        return False

    def get_winner(self) -> str:
        """
        Returns the winner of the game.

        Returns: str : The winner of the game's color, "DRAW" if the game is a
        draw, or "GAME NOT OVER" if the game is not over.
        """
        if not self.is_game_over():
            return "GAME NOT OVER"
        elif (
            len(self.get_valid_player_moves("RED")) == 0
            and self.get_valid_player_moves("BLACK") == 0
        ):
            return "DRAW"
        elif len(self.get_valid_player_moves("RED")) == 0:
            return "BLACK"
        return "RED"
