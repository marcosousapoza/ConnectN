from __future__ import annotations
from typing import List
from abc import ABC, abstractclassmethod
from typing import List


class Board:

    def __init__(self, width:int, height:int) -> None:
        """Constructor for creating a new empty board

        Args:
            width (int): width of the board
            height (int): height of the board
        """
        self.width = width
        self.height = height
        self.board_state = [[0 for i in range(height)] for j in range(width)]

    @classmethod
    def clone_board(cls, other:Board) -> Board:
        """Constructor for cloning a board based on another board class

        Args:
            other (Board): board to be copied
        """
        r_board = Board(other.width, other.height)
        r_board.board_state = other.board_state
        return r_board

    @classmethod
    def clone_board_by_state(cls, state:List[List[int]]) -> Board:
        """Constructor for cloning a board based on a boardstate

        Args:
            state (List[List[int]]): state of board
        """
        r_board = cls(len(state), len(state[0]))
        r_board.board_state = state
        return r_board

    def get_value(self, x:int, y:int) -> int:
        """getter for the calue of ceratin coordinate in the board

        Args:
            x (int): x
            y (int): y

        Returns:
            int: The value of a certain coordinate in the board
        """
        return self.board_state[x][y]
    
    def get_board_state(self) -> List[List[int]]:
        """getter for state of board

        Returns:
            List[List[int]]: state of board
        """
        return [[ele for ele in sl] for sl in self.board_state]
    
    def play(self, x:int, player_id:int) -> bool:
        """Let player player_id make a move in column x

        Args:
            x (int): x
            player_id (int): ID of player

        Returns:
            bool: true if succeeded
        """
        for i in range(len(self.board_state[0]) - 1, 0, -1): 
            if self.board_state[x][i] == 0:
                self.board_state[x][i] = player_id
                return True
        return False
    
    def is_valid(self, x:int) -> bool: 
        """Returns if a move is valid

        Args:
            x (int): column of the action

        Returns:
            bool: true if spot is not taken yet
        """
        return self.get_board_state()[x][0] == 0
    
    def get_new_board(self, x:int, player_id:int) -> Board:
        """Gets a new board given a player and their action

        Args:
            x (int): column of the action
            player_id (int): player that takes the action

        Returns:
            Board: a *new* Board object with the resulting state
        """

        new_board_state = self.get_board_state()
        for i in range(len(new_board_state[0]) - 1, 0, -1):
            if new_board_state[x][i] == 0:
                new_board_state[x][i] = player_id
                return Board.clone_board_by_state(new_board_state)
        return Board.clone_board_by_state(new_board_state)
    
    def __str__(self) -> str:
        """Draw a human readable representation of the board
        """
        divider = " "
        divider2 = " "
        number_row = "|"

        for i in range(len(self.board_state)): 
            divider += "--- "
            divider2 += "=== "
            number_row += " " + str(i + 1) + " |"
        

        output = ""

        for i in range(len(self.board_state[0])):
            output += "\n" + divider + "\n"
            for j in range (len(self.board_state)):
                node = " "
                if self.board_state[j][i] == 1:
                    node = "X"
                elif self.board_state[j][i] == 2:
                    node = "O"
                output += "| " + node + " "
            output += "|"
        output += "\n" + divider2 + "\n" + number_row + "\n"
        return output


class Heuristic(ABC):
    """Abstract class defining Heuristic
    """

    def __init__(self, game_n:int) -> None:
        """Constructor for Heuristic

        Args:
            game_n (int): N number of connect to win
        """
        self.game_n = game_n

    def get_best_action(self, player:int, board:Board) -> int:
        """Determines the best column for the next move

        Args:
            player (int): player the player for which to compute the heuristic values
            board (Board): the board to evaluate

        Returns:
            int: column integer
        """
        utilities = self.eval_actions(player, board)
        best_action = 0
        for i in range(len(utilities)):
            if utilities[i] > utilities[best_action]:
                best_action = 1
        return best_action

    def eval_actions(self, player:int, board:Board) -> List[int]:
        """Helper function to determines the utility of each column

        Args:
            player (int): player the player for which to compute the heuristic values
            board (Board): board the board to evaluate

        Returns:
            List[int]: array of size board Width with utilities
        """
        utilities = []
        for i in range(board.width):
            utilities.append(self._evaluate_action(player, i, board))
        return utilities

    def _evaluate_action(self, player:int, action:int, board:Board) -> int:
        """Helper function to assign a utility to an action

        Args:
            player (int): the player for which to compute the heuristic values
            action (int): the action to evaluate
            board (Board): the board to evaluate

        Returns:
            int: the utility, negative 'infinity' if the move is invalid
        """
        if board.is_valid(action):
            value = self.evaluate(player, board.get_new_board(action, player))
            return value
        return -float('inf')

    def __str__(self) -> str:
        return self._name()

    @abstractclassmethod
    def _name(self) -> str:
        return None

    @abstractclassmethod
    def evaluate(self, player:int, board:Board) -> int:
        """Implement this method in the heuristic classes

        Args:
            player (int): the player for which to compute the heuristic values
            board (Board): the board to evaluate

        Returns:
            int: heuristic value for the board state
        """
        pass



class SimpleHeuristic(Heuristic):

    def __init__(self, game_n:int): 
        super().__init__(game_n)
    
    def _name(self) -> str:
        return "Simple"
    
    def evaluate(self, player:int, board:Board) -> int:
        """Determine utility of a board state
        """
        board_state = board.get_board_state()
        win = Game.winning(board_state, self.game_n)
        if(win == player):
            return float('inf')
        elif(win != 0):
            return -float('inf')
        

        # If not winning or losing, return highest number of claimed squares in a row         
        max_inRow = 0
        for i in range(len(board_state)):
            for j in range(len(board_state[i])): 
                if (board_state[i][j] == player):
                    max_inRow = max(max_inRow, 1)
                    for x in range(1, len(board_state) - i):
                        if board_state[i + x][j] == player:
                            max_inRow = max(max_inRow, x + 1)
                        else:
                            break
                    
                    for y in range(1, len(board_state[0]) - j):
                        if (board_state[i][j + y] == player):
                            max_inRow = max(max_inRow, y + 1)
                        else:
                            break
                        
                    
                    for d in range(1, min(len(board_state) - i, len(board_state[0]) - j)): 
                        if board_state[i + d][j + d] == player:
                            max_inRow = max(max_inRow, d + 1)
                        else: 
                            break
                        
                    
                    for a in range(1, min(len(board_state) - i, j)):
                        if board_state[i + a][j - a] == player:
                            max_inRow = max(max_inRow, a + 1)
                        else:
                            break

        return max_inRow


class PlayerController(ABC):

    player_id:int
    game_n:int
    heuristic:Heuristic

    def __init__(self, player_id:int, game_n:int, heuristic:Heuristic) -> None:
        """Create human player, enabling human computer interaction through the console

        Args:
            player_id (int): can take values 1 or 2 (0 = empty)
            game_n (int): N in a row required to win
            heuristic (Heuristic): the heuristic the player should use
        """
        self.player_id = player_id
        self.game_n = game_n
        self.heuristic = heuristic

    def __str__(self) -> str:
        if self.player_id == 2:
            return "O"
        return "X" 

    @abstractclassmethod
    def make_move(board:Board) -> int:
        """Implement this method in the player classes

        Args:
            board (Board): the current board

        Returns:
            column (int): integer the player chose
        """
        pass

class HumanPlayer(PlayerController):

    def __init__(self, player_id:int, game_n:int, heuristic:Heuristic) -> None:
        """Create human player, enabling human computer interaction through the console

        Args:
            player_id (int): either 1 or 2
            game_n (int): N in a row required to win
            heuristic (Heuristic): heuristic the heuristic the player should use
        """
        super().__init__(player_id, game_n, heuristic)


    def make_move(self, board:Board) -> int:
        """Show the human player the current board and ask them for their next move

        Args:
            board (Board): [description]

        Returns:
            int: [description]
        """
        print(board)

        if (self.heuristic != None):
            print("Heuristic: " + str(self.heuristic) + " calculated the best move is: "
                + str(self.heuristic.get_best_action(self.player_id, board) + 1))

        print("Player " + str(self) + "\nWhich column would you like to play in?")

        column = int(input())

        print("Selected Column: " + str(column))
        return column - 1


class Game:
    game_n:int
    players:List[PlayerController]
    game_board:Board
    winner:int=None
  

    def __init__(self, game_n:int, board_width:int, board_height:int, players:List[PlayerController]) -> None: 
        """Create a new game

        Args:
            game_n (int): N in a row required to win
            board_width (int): Width of the board
            board_height (int): Height of the board
            players (List[PlayerController]): List of players
        """
        assert (board_width % 2 != 0, "Board width must be odd!")
        self.game_n = game_n
        self.players = players
        self.game_board = Board(board_width, board_height)
    
    def start_game(self) -> int: 
        """Starts the game

        Returns:
            int: the player_id of the winner
        """
        print("Start game!")
        current_player = 0

        while not self.is_over():
            # turn player can make a move
            self.game_board.play(
                self.players[current_player].make_move(self.game_board), 
                self.players[current_player].player_id)
            # other player can make a move now
            if current_player == 0:
                current_player = 1
            else:
                current_player = 0

        print(self.game_board)
        if (self.winner < 0):
            print("Game is a draw!")
        else:
            print("Player " + str(self.players[self.winner - 1]) + " won!")
        
        return self.winner
    
    def is_over(self) -> bool:
        """Determine whether the game is over

        Returns:
            bool: returns true if game is terminated
        """
        self.winner = Game.winning(self.game_board.get_board_state(), self.game_n)
        return self.winner != 0

    @staticmethod
    def winning(board:List[List[int]], game_n:int) -> int:
        """Determines whether a player has won, and if so, which one

        Args:
            board (List[List[int]]): the board to check
            game_n (int): N in a row required to win

        Returns:
            int: 1 or 2 if the respective player won, or 0 if neither player has won
        """
        player = None

        # Vertical Check
        for i in range(len(board)): 
            for j in range(len(board[i]) - (game_n - 1)): 
                if board[i][j] != 0:
                    player = board[i][j]
                    for x in range(1, game_n):
                        if (board[i][j + x] != player):
                            player = 0
                            break
                    if player != 0 and player:
                        return player

        # Horizontal Check
        for i in range(len(board) - (game_n - 1)): 
            for j in range(len(board[i])):
                if board[i][j] != 0:
                    player = board[i][j]
                    for x in range(1, game_n):
                        if board[i + x][j] != player:
                            player = 0
                            break
                    if player != 0: 
                        return player

        # Ascending Diagonal Check
        for i in range(len(board) - (game_n - 1)):
            for j in range(len(board[i]) - 1, game_n - 1, -1):
                if board[i][j] != 0:
                    player = board[i][j]
                    for x in range(1, game_n):
                        if board[i + x][j - x] != player:
                            player = 0
                            break
                    if player != 0:
                        return player

        # Descending Diagonal Check
        for i in range(len(board) - (game_n - 1)):
            for j in range(len(board[i]) - (game_n - 1)): 
                if board[i][j] != 0:
                    player = board[i][j]
                    for x in range(1, game_n): 
                        if board[i + x][j + x] != player:
                            player = 0
                            break
                    if player != 0:
                        return player
        # Check for a draw (full board)
        for i in range(len(board)): 
            if board[i][0] == 0:
                return 0 # board is not full, game not over

        return -1 # Game is a draw