import numpy as np
from numpy.lib.type_check import _real_if_close_dispatcher
from . import Heuristic, Board, Game
from typing import List, Optional, Tuple

class BadHeuristic(Heuristic):

    def __init__(self, game_n:int) -> None:
        super().__init__(game_n)
    
    def _name(self) -> str:
        return "Bad"
    
    def evaluate(self, player:int, board:Board) -> int:
        """Determine utility of a board state
        """
        return 0


class SimpleHeuristic(Heuristic):

    def __init__(self, game_n:int): 
        super().__init__(game_n)
    
    def _name(self) -> str:
        return "Simple"
    
    def evaluate(self, player:int, board:Board) -> int:
        """Determine utility of a board state
        """

        # If winning or losing evaluation is easy
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
        # if best move is not valid we choose a random one
        while not board.is_valid(max_inRow):
            max_inRow = (max_inRow + 1) % board.width
        return max_inRow


class BetterHeuristic(Heuristic):

    def __init__(self, game_n:int) -> None:
        super().__init__(game_n)

    def _name(self) -> str:
        return "Better"

    def evaluate(self, player: int, board: Board) -> int:

        def get_diagnoal_lr(state:np.ndarray) -> List[List[int]]:
            rArray = []
            for i in range(1-len(state), len(state[0])):
                rArray.append(state.diagonal(offset=i).tolist())
            return rArray

        def get_diagonal_rl(state:np.ndarray) -> List[List[int]]:
            rArray = []
            for i in range(1-len(state[0]), len(state)):
                rArray.append(np.fliplr(state).diagonal(offset=i).tolist())
            return rArray

        def get_columns(state:np.ndarray) -> List[List[int]]:
            return state.tolist()

        def get_rows(state:np.ndarray) -> List[List[int]]:
            return state.T.tolist()

        def get_all(state:np.ndarray):
            rList = []
            for row in get_diagnoal_lr(state):
                rList.append(row)
            for row in get_diagonal_rl(state):
                rList.append(row)
            for row in get_columns(state):
                rList.append(row)
            for row in get_rows(state):
                rList.append(row)
            return rList

        def connectin_options(board:List[List[int]]) -> int:
            for x, col in enumerate(board):
                for y, row in enumerate(col):
                    pass #TODO
            return 0

        def enclosedness(row:List[int], index:int) -> int:
            """coefficient for how accessible row is for player

            Args:
                row (List[int]): row
                index (int): index of tile

            Returns:
                int: 0, 1 or 2
            """
            rvalue = 2
            cur_ele = row[index]
            for i in range(index, len(row)):
                if row[i] != cur_ele:
                    rvalue -= 1
                    break
                if row[i] == 0:
                    break
                if i == len(row) - 1:
                    rvalue -= 1
            for i in range(index, -1, -1):
                if row[i] != cur_ele:
                    rvalue -= 1
                    break
                if row[i] == 0:
                    break
                if i == 0:
                    rvalue -= 1
            return rvalue

        def max_length(row:List[int], player_id:int) -> Tuple[int, int]:
            rint = 0
            mxint = 0
            index = -1
            for i in range(len(row)):
                if row[i] == player_id:
                    rint += 1
                else:
                    mxint = max(rint, mxint)
                    if mxint > 0:
                        index = i-1
                    rint = 0
            return (max(rint, mxint), index)
                
        # If winning or losing evaluation is easy
        board_state = board.get_board_state()
        win = Game.winning(board_state, self.game_n)
        if(win == player):
            return float('inf')
        elif(win != 0):
            return -float('inf')

        heur_value = 0
        for row in get_all(board.get_board_state_array()):
            m, i = max_length(row, player)
            if i != -1:
                heur_value += m*enclosedness(row, i)
            m, i = max_length(row, board.get_opponent(player))
            if i != -1:
                heur_value -= m*enclosedness(row, i)
        return heur_value


class BetterHeuristic2(Heuristic):

    def __init__(self, game_n: int) -> None:
        super().__init__(game_n)

    def _name(self) -> str:
        return "Better 2"

    def evaluate(self, player: int, board: Board) -> int:
        
        def connectability(state:List[List[int]], col:int, row:int, pl_id:int) -> int:
            val = 0
            if row - 1 > 0 and (state[row-1][col] == pl_id or state[row-1][col] == 0):
                val += 1
            if row + 1 < len(state) and (state[row+1][col] == pl_id or state[row+1][col] == 0):
                val += 1
            if col + 1 < len(state[0]) and (state[row][col+1] == pl_id or state[row][col+1] == 0):
                val += 1
            # diagonal check
            if row - 1 > 0 and col - 1 > 0 and (state[row-1][col-1] == pl_id or state[row-1][col-1] == 0):
                val += 1
            if row - 1 > 0 and col + 1 < len(state[0]) and (state[row-1][col+1] == pl_id or state[row-1][col+1] == 0):
                val += 1
            if row + 1 < len(state) and col + 1 < len(state[0]) and (state[row+1][col+1] == pl_id or state[row+1][col+1] == 0):
                val += 1
            if row + 1 < len(state) and col - 1 > 0 and (state[row+1][col-1] == pl_id or state[row+1][col-1] == 0):
                val += 1
            return val
        
        # If winning or losing evaluation is easy
        board_state = board.get_board_state()
        win = Game.winning(board_state, self.game_n)
        if(win == player):
            return float('inf')
        elif(win != 0):
            return -float('inf')

        heur_value = 0
        oppnt = board.get_opponent(player)
        moves_player = board.moves_played(player)
        moves_oppnet = board.moves_played(oppnt)

        for i in range(len(board_state)):
            for j in range(len(board_state[0])):
                if board_state[i][j] == player:
                    heur_value += connectability(board_state, j, i, player)/moves_player
                elif board_state[i][j] == oppnt:
                    heur_value -= connectability(board_state, j, i, player)/moves_oppnet

        return heur_value