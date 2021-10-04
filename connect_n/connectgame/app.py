from . import Game, PlayerController
from .heuristics import BadHeuristic, BetterHeuristic, BetterHeuristic2, SimpleHeuristic
from .controllers import AlphaBeta, HumanPlayer, MinMax
from typing import List

class App:

    @staticmethod
    def launch() -> None:
        """lauches the game
        """
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
            List[PlayerController]: an array of size 2 with two Playercontrollers
        """

        # use fast heuristic
        heuristic1 = BetterHeuristic2(n)
        heuristic2 = BetterHeuristic2(n)

        compu1 = AlphaBeta(1, n, heuristic1, 6)
        compu2 = AlphaBeta(2, n, heuristic2, 6)

        players =  [compu1, compu2] 

        return players