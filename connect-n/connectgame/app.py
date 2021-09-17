from . import Game, SimpleHeuristic, HumanPlayer, PlayerController
from typing import List

class App:

    @staticmethod
    def launch() -> None:
        game_n = 4
        board_width = 7
        board_height = 6

        players = App._get_players(game_n)

        game = Game(game_n, board_width, board_height, players)
        game.start_game()


    @staticmethod
    def _get_players(n:int) -> List[PlayerController]:
        """Determine the players for the game
        Returns:
            [type]: an array of size 2 with two Playercontrollers
        """
        heuristic1 = SimpleHeuristic(n)
        heuristic2 = SimpleHeuristic(n)

        human = HumanPlayer(1, n, heuristic1)
        human2 = HumanPlayer(2, n, heuristic2)

        #TODO: Implement other PlayerControllers (MinMax, AlphaBeta)

        players =  human, human2 

        return players