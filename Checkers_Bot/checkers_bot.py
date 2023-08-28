from game_logic import Board, Piece, PieceColor, Checkers
import copy
import random


class RandomBot:
    """
    A game playing bot for the game of checkers which picks a random move out of
    a list of possible moves.
    """
    def __init__(self, checkers, color) -> None:
        """
        Constructor function for the random checkers bot.

        Parameters:
            checkers: Checkers Object: the checkers object that the bot will
                play on
            color : PieceColor : The color of the piece.
        """
        self.checkers = checkers
        self.color = color

    def find_move(self):
        """
        Given a board and a player, it will generate a random possible next move
        for that player to make.

        Returns:
            (start, destination): tuple(tuple(int, int), tuple(int, int)): a
                start and end destination correlating to the piece move
        """
        possible_moves = self.checkers.get_valid_player_moves(self.color)
        start, destinations = random.choice(list(possible_moves.items()))
        destination = random.choice(destinations)
        return (start, destination)

class SmartBot:
    """
    A game playing bot for the game of checkers which look at a checkers board
    and will return a move based upon a set evaluation method for each move.
    """

    def __init__(self, checkers, color) -> None:
        """
        Constructor function for the checkers bot.

        Parameters:
            checkers: Checkers Object: the checkers object that the bot will
                play on
            color : PieceColor : The color of the piece.
        """
        self.checkers = checkers
        self.color = color

    def find_move(self, board, color):
        """
        This will have the bot return a move that it belives is the best move.

        Parameters:
            board: Checkers: 
            color: Enum: the color of the pieces that they would like to move

        Returns:
            move: tuple(tuple(int, int), tuple(int, int)): a
                start and end destination correlating to the piece move
        """
        possible_moves = board.get_valid_player_moves(color)
        if color == "RED":
            jumps = board.get_jump_moves("BLACK")
        else:
            jumps = board.get_jump_moves("RED")
        blocks = self.check_for_jump_blocks(possible_moves, jumps)
        # If you are about to get jumped and can prevent it, you should do so.
        # If you can prevent multiples jumps, or one jump in multipple ways,
        # then perform the move with the highest score
        if len(blocks) != 0:
            return self.highest_score_move(blocks)
        king_moves = self.will_make_king(possible_moves)
        # If you can make a king, then do it. If you can make more than one than
        # perform the kinging move with the highest score
        if len(king_moves) != 0:
            return self.highest_score_move(king_moves)
        # If you are not about to get jumped and you cannot make a king
        # then find the move with the highest score
        return self.highest_score_move(possible_moves)

    def find_opp_move(self, board, color):
        """
        This will have the bot return a move that it belives is the best move.

        Parameters:
            board: Checkers: 
            color: Enum: the color of the pieces that they would like to move

        Returns:
            move: tuple(tuple(int, int), tuple(int, int)): a
                start and end destination correlating to the piece move
        """

        possible_moves = board.get_valid_player_moves(color)
        if color == "RED":
            jumps = board.get_jump_moves("BLACK")
        else:
            jumps = board.get_jump_moves("RED")
        blocks = self.check_for_jump_blocks(possible_moves, jumps)
        if len(blocks) != 0:
            return self.highest_opp_score_move(blocks, board)
        king_moves = self.will_make_king(possible_moves)
        if len(king_moves) != 0:
            return self.highest_opp_score_move(king_moves, board)
        return self.highest_opp_score_move(possible_moves, board)

    def highest_score_move(self, moves):
        """
        Takes in a list of moves and returns the move with the highest
        calculated score.

        Parameters:
            moves: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible move
                and values that are a list of possible ending coordinates for a
                move with said starting coordinate
        
        Returns: 
            final_move: tuple(tuple(int, int), tuple(int, int)): a start
                and end destination correlating to the piece move
        """
        max_score = -1000000
        final_move = None
        for start_coord, destinations in moves.items():
            for destination in destinations:
                score = self.evaluate_move(self.checkers, (start_coord, destination))
                if score > max_score:
                    max_score = score
                    final_move = (start_coord, destination)
        return final_move
        
    def highest_opp_score_move(self, moves, board):
        """
        Takes in a list of moves and returns the move with the highest
        calculated score.

        Parameters:
            moves: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible move
                and values that are a list of possible ending coordinates for a
                move with said starting coordinate
            board: Checkers: 
        
        Returns: 
            final_move: tuple(tuple(int, int), tuple(int, int)): a start
                and end destination correlating to the piece move
        """
        max_score = -1000000
        final_move = None
        # print(moves)
        for start_coord, destinations in moves.items():
            for destination in destinations:
                score = self.evaluate_move(board, (start_coord, destination))
                if score > max_score:
                    max_score = score
                    final_move = (start_coord, destination)
        return final_move

    def highest_five(self, board, moves, square_values):
        """
        Takes in a list of moves and returns the list of moves with the five highest
        calculated scores.

        Parameters:
            moves: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible move
                and values that are a list of possible ending coordinates for a
                move with said starting coordinate
        
        Returns: 
            final_move: tuple(tuple(int, int), tuple(int, int)): a start
                and end destination correlating to the piece move
        """
        max_scores = [(-1000, None)] * 5
        for start_coord, destinations in moves.items():
            for destination in destinations:
                score = self.evaluate_move(board, (start_coord, destination))
                if score > max_scores[0][0]:
                    max_scores.append((score, (start_coord, destination)))
                    max_scores.sort(reverse=True)
                    max_scores.pop()
        final_moves = [score for score, _ in max_scores]
        return final_moves

    def check_for_jump_blocks(self, moves, jumps):
        """
        Takes in a list of possible moves and a list of jumps that are being
        threatened and returns a list of moves that will block these jumps.

        Parameters:
            moves: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible move
                and values that are a list of possible ending coordinates for a
                move with said starting coordinate
            jumps: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible
                threatend jump and values that are a list of possible ending
                coordinates for the jump with said starting coordinate
        
        Returns:
            blocks: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a blocking move
                and values that are a list of possible ending coordinates for
                that blocking move
        """
        blocks = {}
        if jumps != {}:
            for jump_lands in jumps.values():
                for jump_land in jump_lands:
                    if self.check_for_move_land_blocks(jump_land, moves) is\
                            None:
                        return {}
                    (move_start, move_land) = \
                        self.check_for_move_land_blocks(jump_land, moves)
                    blocks[move_start] = [move_land]
        return blocks
    
    def check_for_move_land_blocks(self, jump_land, moves):
        """
        Helper function for check_for_jump_blocks which takes in the same
        parameters and checks to see if the player has any possible moves to
        block the threatened jumps

        Parameters:
            moves: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible move
                and values that are a list of possible ending coordinates for a
                move with said starting coordinate
            jumps: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible
                threatend jump and values that are a list of possible ending
                coordinates for the jump with said starting coordinate

        Returns:
            (move_start, move_land): tuple(tuple(int, int), tuple(int, int)): a
                start and end destination for your blocking move
        """
        for move_start, move_lands in moves.items():
            for move_land in move_lands:
                if jump_land == move_land:
                    return (move_start, move_land)
  
    def will_make_king(self, moves):
        """
        Takes in a list of moves and check to see if any of them will end up
        making a king.

        Parameters:
            moves: dict{tuple(int, int): list[tuple(int, int)]}: a dictionary
                with keys that are the starting coordinates of a possible move
                and values that are a list of possible ending coordinates for a
                move with said starting coordinate
        
        Returns:
            king_moves: dict{tuple(int, int): list[tuple(int, int)]}: a dict
                with keys that are the starting coordinates of a possible
                kinging moves and values that are a list of possible ending
                coordinates for said kinging moves
        """
        king_moves = {}
        for start_coord, destinations in moves.items():
            for destination in destinations:
                if self.checkers._board._get_square(start_coord).get_color() ==\
                        "RED" and destination[0] ==\
                        self.checkers._board._rows - 1:
                    king_moves[start_coord] = king_moves.get(start_coord, []) +\
                        [destination]
                elif self.checkers._board._get_square(start_coord).get_color()\
                        == "BLACK" and destination[0] == 0:
                    king_moves[start_coord] = king_moves.get(start_coord, []) +\
                        [destination]
        return king_moves

    def find_black_square_values(self):
        """
        Calculates a value for each square on the board for a player with the
        color Black, incentivising controling the middle, maintaing a strong
        back row, and pushing your pieces forwards in order to make kings.

        Returns:
            black_square_values: dict{tuple(int, int): int}: a dict with the
                keys as the coordinates of each square and the values as the int
                representitive of the value of that square for a player with the
                color Black
        """
        black_square_values = {}
        rows = self.checkers._board._rows
        columns = self.checkers._board._columns
        row = 0
        column = 0
        square_value = 94
        cur_row = 0
        final_row = False
        for row in range(rows):
            for column in range(columns):
                black_square_values[(row, column)] = None
        for cord in black_square_values:
            # Incentivise maintaining a strong back row
            if cord[0] == (rows - 1) and final_row == False:
                square_value += int(10 * ((rows / 2) + 1))
                final_row = True
            # Incentivise pushing forwards to make kings
            if cur_row != cord[0]:
                square_value -= 10
                cur_row = cord[0]
            # Incentivise taking control of the center of the board
            if cord[1] <= (columns / 2):
                square_value += 1
                black_square_values[cord] = square_value
            if cord[1] > (columns / 2):
                square_value -= 1
                black_square_values[cord] = square_value
        return black_square_values

    def find_red_square_values(self):
        """
        Calculates a value for each square on the board for a player with the
        color Red, incentivising controling the middle, maintaing a strong back
        row, and pushing your pieces forwards in order to make kings.

        Returns:
            red_square_values: dict{tuple(int, int): int}: a dict with the
                keys as the coordinates of each square and the values as the int
                representitive of the value of that square for a player with the
                color Red
        """
        square_values = self.find_black_square_values()
        vals = []
        count = 0
        for value in square_values.values():
            vals.append(value)
        for i in range(len(vals) // 2):
            vals[i], vals[(-i) - 1] = vals[(-i) - 1], vals[i]
        for key in square_values:
            square_values[key] = vals[count]
            count += 1
        return square_values

    def piece_positional_score(self, checkers, piece, square_values):
        """
        Calculated the positional score a piece on the board according to the
        value of the square it is on, the number of same-colored pieces around
        it, and if it can jump and opposing piece while not being able to be
        jumped itself.

        Parameters:
            checkers: Checkers: the checkers object that corresponds to
                the board on which you are calculating the piece score
            piece: Piece: the piece that you are attempting to calculate the
                score for
            square_values: dict{tuple(int, int): int}: the square values of that
                sized board and for the color that the piece is
        
        Returns:
            pos_score: int: the positional score of the piece on the board
        """
        pos_score = 0
        if self.color == "RED":
            opp_color = "BLACK"
        else:
            opp_color = "RED"
        cords = piece.get_coordinates()
        # Add the value of the square to the positional score
        pos_score += square_values[cords]
        surrounding_squares = [(max((cords[0] - 1), 0), max((cords[1] - 1), 0)),
                                (min((cords[0] + 1),\
                                    (checkers._board._rows - 1)),\
                                    max((cords[1] - 1), 0)),
                                (max((cords[0] - 1), 0), min((cords[1] + 1),\
                                    (checkers._board._columns - 1))),
                                (min((cords[0] + 1),\
                                    (checkers._board._rows - 1)),\
                                    min((cords[1] + 1),\
                                    (checkers._board._columns - 1)))]
        # In case pieces in the corners of the board accidentally add themselves
        # as a surrounding square
        if cords in surrounding_squares:
            surrounding_squares.remove(cords)
        for square in surrounding_squares:
            square = checkers._board._get_square(square)
            if square:
                # Add value to the positional score based upon the numer of same
                # colored pieces around it to incentivise pushing your pieces
                # together
                if square.get_color() == piece.get_color:
                    pos_score += 75
                # Adds value to the positional score when the piece can jump an
                # opposing piece but cannot be jumped themselves
                if cords in checkers.get_jump_moves(self.color) and not \
                        checkers.has_jump_move(opp_color):
                    pos_score += 75
        return pos_score

    def evaluate_move(self, board, move) -> int:
        """
        Takes a potential move and outputs an int which is a score for how good
        the move is to make.
        
        Parameters:
            board: Checkers: the board that the move is being evaluated on
            move: tuple(tuple(int, int), tuple(int, int)): the potential move
                that is being evaluated
        
        Returns:
            score: int: the score that is associated with that potential move
        """
        (start, destination) = move
        if self.color == "RED":
            square_values = self.find_red_square_values()
        else:
            square_values = self.find_black_square_values()
        cur_score = self.piece_positional_score(board,\
                        board._board._get_square(start), square_values)
        temp_checkers = copy.deepcopy(board)
        try:
            temp_checkers.move_piece(start, destination)
        except Exception:
            # print(temp_checkers)
            # print((start, destination))
            raise Exception()
        new_score = self.piece_positional_score(temp_checkers,\
                        temp_checkers._board._get_square(destination),\
                        square_values)
        return new_score

    def two_level_evaluate_move(self, move) -> int:
        """
        Takes a potential move and outputs an int which is a score for how good
        the move is to make.
        
        Parameters:
            move: tuple(tuple(int, int), tuple(int, int)): the potential move
                that is being evaluated
        
        Returns:
            score: int: the score that is associated with that potential move
        """
        (start, destination) = move
        total = 0
        if self.color == "RED":
            square_values = self.find_red_square_values()
            opp_col = "BLACK"
        else:
            square_values = self.find_black_square_values()
            opp_col = "RED"
        cur_score = self.piece_positional_score(self.checkers,\
                        self.checkers._board._get_square(start), square_values)
        temp_checkers = copy.deepcopy(self.checkers)
        temp_checkers.move_piece(start, destination)
        if temp_checkers.is_game_over:
            return 100000000
        # print("\nPOSSIBLE OPP MOVE\n")
        # print(temp_checkers)
        new_score = self.piece_positional_score(temp_checkers,\
                        temp_checkers._board._get_square(destination),\
                        square_values)
        # if opp_col == "BLACK":
        #     self.checkers._whose_turn = "BLACK"
        # else:
        #     self.checkers._whose_turn = "RED"
        opp_start, opp_destination = self.find_opp_move(temp_checkers, opp_col)
        temp_checkers.move_piece(opp_start, opp_destination)
        # print("\nLIST OF SECOND MOVES\n")
        # print(temp_checkers.get_valid_player_moves(self.color))
        second_move_score = self.highest_five(temp_checkers, temp_checkers.get_valid_player_moves(self.color), square_values)
        total = (.5 * (new_score)) + (.5 * (((sum(second_move_score))/5) + new_score))
        # print("\nIt's Second Move Score was: ")
        # print(total)
        # print("\n")
        return total - cur_score

class BotTest:
    """
    This will play a random bot against a smart bot in 'n' games of checkers.
    """
    def __init__(self):
        """
        Construcor for the bot test
        """
        pass

    def run_test(self, trials = 100):
        """
        Runs 'trails' games of a smart bot against a random bot and returns the
        win percentages, the default number of trials is 100.

        Parameters:
            trials: int | default = 100: the number of games you would like the
                bots to play
        """
        smart_bot_wins = 0
        rand_bot_wins = 0
        draws = 0
        for n in range(trials):
            checkers = Checkers()
            smart = SmartBot(checkers, random.choice(["RED", "BLACK"]))
            if smart.color == "RED":
                rand = RandomBot(checkers, "BLACK")
            else:
                rand = RandomBot(checkers, "RED")
            while not checkers.is_game_over():
                # print(checkers)
                # print("\n")
                if checkers.get_whose_turn() == smart.color and not\
                        checkers.is_game_over():
                    # print("\nBOT'S TURN\n")
                    start, destination = smart.find_move(smart.checkers, smart.color)
                    # print("\nBOT FINAL MOVE\n")
                    checkers.move_piece(start, destination)
                if checkers.get_whose_turn() == rand.color and not\
                        checkers.is_game_over():
                    start, destination = rand.find_move()
                    checkers.move_piece(start, destination)
            if checkers.get_winner() == smart.color:
                smart_bot_wins += 1
            if checkers.get_winner() == rand.color:
                rand_bot_wins += 1
            if checkers.get_winner() == "DRAW":
                draws += 1
            smart_win_percent = float((smart_bot_wins / \
                                (smart_bot_wins + rand_bot_wins + draws))) * 100
            rand_win_percent = float((rand_bot_wins / \
                                (smart_bot_wins + rand_bot_wins + draws))) * 100
            draw_percent = float((draws / trials)) * 100
        # print(f"The SmartBot won {smart_win_percent}% of the games.\n" +\
        #       f"The RandBot won {rand_win_percent}% of the games.\n" +\
        #       f"There were {draw_percent}% draws.")
        return smart_win_percent, rand_win_percent