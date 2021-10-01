from connect_n.connectgame import heuristics
from . import PlayerController, Heuristic, Board, Game, Tree
from typing import Optional
from time import sleep

class HumanPlayer(PlayerController):

    def __init__(self, player_id:int, game_n:int, heuristic:Optional[Heuristic]) -> None:
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


class MinMax(PlayerController):

    def __init__(self, player_id:int, game_n:int, heuristic:Heuristic, depth:int):
        assert heuristic != None, "The computer player needs a heuristic to" 
        "calculate the move but has not received any"
        self.depth = depth
        super().__init__(player_id, game_n, heuristic)

    def __min_max(self, node:Tree, depth:int) -> float:
        if depth == 0 or node.is_terminal():
            node.approximate(self.heuristic)
            return node.evaluate()
        if node.get_player() == self.player_id:
            value = -float('inf')
            for child in node.get_children():
                value =  max(self.__min_max(child, depth-1), value)
            return value
        else:
            value = float('inf')
            for child in node.get_children():
                value = min(self.__min_max(child, depth-1), value)
            return value

    def make_move(self, board:Board) -> int:
        print(board)

        # create Tree structure
        tree = Tree(board, self.player_id, self.game_n)
        children = tree.get_children()

        # if there is only one move the descision is made fast
        if len(children) == 1:
            return children[0].get_transition_move()

        best = children[0]
        for child in children:
            child.set_evaluation(    
                self.__min_max(
                    child, 
                    self.depth, 
                )
            )
            if child >= best:
                best = child
        return best.get_transition_move()


class AlphaBeta(PlayerController):

    def __init__(self, player_id:int, game_n:int, heuristic:Heuristic, depth:int):
        assert heuristic != None, "The computer player needs a heuristic to" 
        "calculate the move but has not received any"
        self.depth = depth
        super().__init__(player_id, game_n, heuristic)

    def __alphabeta(self, node:Tree, depth:int, alpha:int, beta:int):
        if depth == 0 or node.is_terminal():
            node.approximate(self.heuristic)
            evaluation = node.evaluate()
            return evaluation
        if node.get_player() == self.player_id:
            value = -float('inf')
            for child in node.get_children():
                value = max(value, self.__alphabeta(child, depth-1, alpha, beta))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = float('inf')
            for child in node.get_children():
                value = min(value, self.__alphabeta(child, depth-1, alpha, beta))
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value

    def make_move(self, board: Board) -> int:
        print(board)

        # create Tree structure
        tree = Tree(board, self.player_id, self.game_n)
        children = tree.get_children()

        # if there is only one move the descision is made fast
        if len(children) == 1:
            return children[0].get_transition_move()

        best = children[0]
        for child in children:
            child.set_evaluation(    
                self.__alphabeta(
                    child, 
                    self.depth,
                    -float('inf'),
                    float('inf')
                )
            )
            if child >= best:
                best = child
        return best.get_transition_move()