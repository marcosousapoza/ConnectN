from connect_n.connectgame import heuristics
from . import PlayerController, Heuristic, Board, Game, Node
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

        # initialize attributes
        self.depth = depth

        # counter attributes
        self.counter = 0

        # for silencing output
        self.show = True

        super().__init__(player_id, game_n, heuristic)

    def display(self, b:bool) -> None:
        """if set to false the player will not display the board after move

        Args:
            b (bool): if true the board will be displayed. If false not.
        """
        self.show = b

    def get_counter(self) -> int:
        """gets count of nodes visited

        Returns:
            int: nodes visited
        """
        return self.counter

    def __min_max(self, node:Node, depth:int) -> float:
        """runs min-max on starting node

        Args:
            node (Node): starting node
            depth (int): depth

        Returns:
            float: evaluation
        """
        self.counter += 1
        if depth == 0 or node.is_terminal():
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
        """makes a move on board

        Args:
            board (Board): current position

        Returns:
            int: best move
        """
        if self.show:
            print(board)

        # create Node structure
        tree = Node(board, self.player_id, self.game_n, self.heuristic)
        children = tree.get_children()

        # reset counter
        self.counter = 0

        # if there is only one move the descision is made fast
        if len(children) == 1:
            return children[0].get_last_move()

        best = children[0]
        best_eval = -float('inf')
        for child in children:
            new_eval = self.__min_max(
                                child, 
                                self.depth-1, 
                            )
            if best_eval < new_eval:
                best = child
                best_eval = new_eval

        if self.show:
            print("Player " + str(self) + " visited " + str(self.counter) + " nodes using the MinMax algorithm")
            print("Player " + str(self) + " selected move " + str(best.get_last_move()))
        
        return best.get_last_move()


class AlphaBeta(PlayerController):

    def __init__(self, player_id:int, game_n:int, heuristic:Heuristic, depth:int):
        assert heuristic != None, "The computer player needs a heuristic to" 
        "calculate the move but has not received any"
        
        # initialize attributes
        self.depth = depth

        # counter attributes
        self.counter = 0
        self.prune_count = 0

        # silence output to terminal
        self.show = True

        super().__init__(player_id, game_n, heuristic)

    def display(self, b:bool) -> None:
        """if set to false the player will not display the board after move

        Args:
            b (bool): if true the board will be displayed. If false not.
        """
        self.show = b

    def get_counter(self) -> int:
        """gets count of nodes visited

        Returns:
            int: nodes visited
        """
        return self.counter

    def get_prune_counter(self) -> int:
        """gets count of pruned branches

        Returns:
            int: pruned branches
        """
        return self.prune_count

    def __alphabeta(self, node:Node, depth:int, alpha:int, beta:int) -> int:
        """runs alpha-beta on starting node

        Args:
            node (Node): starting node
            depth (int): depth
            alpha (int): alpha value
            beta (int): beta value

        Returns:
            int: evaluation
        """
        self.counter += 1
        if depth == 0 or node.is_terminal():
            return node.evaluate()
        if node.get_player() == self.player_id:
            value = -float('inf')
            for child in node.get_children():
                value = max(value, self.__alphabeta(child, depth-1, alpha, beta))
                if value >= beta:
                    self.prune_count += 1
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = float('inf')
            for child in node.get_children():
                value = min(value, self.__alphabeta(child, depth-1, alpha, beta))
                if value <= alpha:
                    self.prune_count += 1
                    break
                beta = min(beta, value)
            return value

    def make_move(self, board: Board) -> int:
        """makes a move on board

        Args:
            board (Board): current position

        Returns:
            int: best move
        """
        if self.show:
           print(board)

        # create Node structure
        tree = Node(board, self.player_id, self.game_n, self.heuristic)
        children = tree.get_children()

        # set counter to 0
        self.counter = 0
        self.prune_count = 0

        # if there is only one move the descision is made fast
        if len(children) == 1:
            return children[0].get_last_move()

        best = children[0]
        best_eval = -float('inf')
        for child in children:
            new_eval = self.__alphabeta(
                child, 
                self.depth-1,
                -float('inf'),
                float('inf')
            )
            
            if best_eval < new_eval:
                best = child
                best_eval = new_eval

        if self.show:
            print("Player " + str(self) + " visited " + str(self.counter) + " nodes using Alpha Beta pruning")
            print("It pruned " + str(self.prune_count) + " branches.")
            print("Player " + str(self) + " selected move " + str(best.get_last_move()))

        return best.get_last_move()