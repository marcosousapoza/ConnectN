from . import PlayerController, Heuristic, Board


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