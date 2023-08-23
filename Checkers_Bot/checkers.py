"""
This module contains the classes and functions necessary to play a game of
checkers.

Classes:
    PieceColor : Enum : An enum representing the color of a piece.
    PlayerColor : Enum : An enum representing the color of a player.
    Player : Class : A class representing a player in a game of checkers.
    Piece : Class : A class representing a piece in a game of checkers.
    Board : Class : A class representing a game board in a game of checkers.

Examples:
    raouf = Player("Raouf", PlayerColor.RED)
    stone = Player("Stone", PlayerColor.BLACK)
    board = Board(player_1, player_2)
    board.is_valid_move((0, 1), (0, 2)) -> False
    board.get_piece_move((1, 2)) -> [(0, 3), (2, 3)]
    board.get_all_player_moves(stone) -> [(Piece1, (1, 4)), ..., (Piece4, (7, 4))]
    board.is_game_over() -> False
    board.get_winner() -> None
"""

from enum import Enum


class PieceColor(Enum):
    """
    Enum representing the color of a piece.
    """

    RED = 1
    BLACK = 2


class PlayerColor(Enum):
    """
    Enum representing the color of a player.
    """

    RED = 1
    BLACK = 2


class Piece:
    """
    Class representing a piece in a game of checkers.
    """

    def __init__(
        self, color: PieceColor, row: int, column: int, is_king: bool = False
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
        self._row = row
        self._column = column
        self._is_king = is_king


class Player:
    """
    Class representing a player in a game of checkers.
    """

    def __init__(self, name: str, color: PlayerColor) -> None:
        """
        Constructor for a player object.

        Parameters:
            name : str : The player's name.
            color : PlayerColor : the player's color.
        """
        self.name = name
        self._color = color
        self._pieces = (
            {}
        )  # dict : a dictionary containing a player's pieces (values) and their coordinates (keys)

    def get_color(self) -> PlayerColor:
        """
        Get a player's color.

        Returns:
            color : PlayerColor : The player's color
        """
        raise NotImplementedError

    def get_pieces(self) -> list[Piece]:
        """
        Get all of a player's pieces.

        Returns:
            pieces : list[Piece] : a list of all of a player's pieces
        """
        raise NotImplementedError


class Board:
    """
    Class representing a game board in a game of checkers.
    """

    def __init__(self, player_1: Player, player_2: Player, size: int = 3) -> None:
        """
        Constructor that constructs a new game board with pieces.

        Parameters:
            player_1 : Player : Player one
            player_2 : Player : Player two
            size : int : The number of rows of pieces a player starts with to begin the game
        """
        self.player_1 = player_1
        self.player_2 = player_2
        self._rows = 2 * size + 2  # int : the total number of rows on the board
        self._columns = 2 * size + 2  # int : the total number of columns on the board
        self._board = (
            self._create_board()
        )  # list[list[Piece | None]] : A 2D matrix represnting the game board

    def _create_board(self) -> list[list[Piece | None]]:
        """
        Generates a fresh game board with 2 * designated size + 2 rows and columns
        and the pieces in their starting positions.

        Returns: list[list[Piece | None]] : A two-dimensional matrix represnting
        a game board, where each element is either a Piece or None.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Returns a string representation of the board.

        Returns: str : A string representation of the board.
        """
        raise NotImplementedError

    def is_valid_move(
        self,
        piece_coordinates: tuple[int, int],
        destination_coordinates: tuple[int, int],
    ) -> bool:
        """
        Checks if a move is valid.

        Parameters:
            piece_coordinates : tuple[int, int] : The coordinates of the piece
            to be moved.
            destination_coordinates : tuple[int, int] : The coordinates of the
            destination of the piece.

        Returns: bool : Whether or not the move is valid.
        """
        raise NotImplementedError

    def get_piece_moves(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Gets all valid moves for a piece.

        Parameters:
            piece : Piece : The piece whose moves are being checked.

        Returns: list[tuple[int, int]] : A list of coordinates that the piece
        can move to.
        """
        raise NotImplementedError

    def get_all_player_moves(
        self, player: Player
    ) -> list[tuple[Piece, tuple[int, int]]]:
        """
        Gets all valid moves for a player.

        Parameters:
            player : Player : The player whose moves are being checked.

        Returns: list[tuple[Piece, tuple[int, int]]] : A list of
        """
        raise NotImplementedError

    def move_piece(self, piece: Piece, destination: tuple[int, int]) -> None:
        """
        Moves a piece to a destination.

        Parameters:
            piece : Piece : The piece to be moved.
            destination : tuple[int, int] : The coordinates of the destination.
        """
        # will use _should_be_king method to check if the piece needs to be updated.
        raise NotImplementedError

    def get_winner(self) -> Player | None:
        """
        Checks whether or not the game is over and who won.

        Returns:
            Player | None : None if the game is not over, or a player
            if someone has won.
        """
        raise NotImplementedError

    def is_game_over(self) -> bool:
        """
        Checks whether or not the game is over.

        Returns:
            bool : True if the game is over, false otherwise.
        """
        raise NotImplementedError

    def _should_be_king(self, piece: Piece) -> None:
        """
        Checkes whether or not a piece should be a king, and, if so, updates it.
        """
        raise NotImplementedError
