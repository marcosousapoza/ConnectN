from . import Heuristic, Board, Game

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