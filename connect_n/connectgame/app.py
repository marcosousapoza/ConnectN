from . import Game, PlayerController
from .heuristics import BadHeuristic, BetterHeuristic, BetterHeuristic2, SimpleHeuristic
from .controllers import AlphaBeta, HumanPlayer, MinMax
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt


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
    def _get_min_max(n:int, depth:int) -> List[MinMax]:
        """get 2 minmax agents

        Args:
            n (int): gamen
            depth (int): depth

        Returns:
            List[MinMax]: list of minmax agents
        """
        # use fast heuristic
        heuristic1 = BetterHeuristic2(n)
        heuristic2 = BetterHeuristic2(n)

        compu1 = MinMax(1, n, heuristic1, depth)
        compu1.display(False)
        compu2 = MinMax(2, n, heuristic2, depth)
        compu2.display(False)

        players =  [compu1, compu2] 

        return players

    @staticmethod
    def _get_alpha_beta(n:int, depth:int) -> List[AlphaBeta]:
        """gets two alpha-beta agents

        Args:
            n (int): gamen
            depth (int): depth

        Returns:
            List[AlphaBeta]: list of alpha-beta agnts
        """
        # use fast heuristic
        heuristic1 = BetterHeuristic2(n)
        heuristic2 = BetterHeuristic2(n)

        compu1 = AlphaBeta(1, n, heuristic1, depth)
        compu1.display(False)
        compu2 = AlphaBeta(2, n, heuristic2, depth)
        compu2.display(False)

        players =  [compu1, compu2] 

        return players

    @staticmethod
    def _get_players(n:int) -> List[PlayerController]:
        """Determine the players for the game
        Returns:
            List[PlayerController]: an array of size 2 with two Playercontrollers
        """

        # use fast heuristic
        heuristic1 = BetterHeuristic2(n)
        heuristic2 = BetterHeuristic2(n)

        compu1 = AlphaBeta(1, n, heuristic1, 8)
        compu2 = HumanPlayer(2, n, heuristic2)

        players =  [compu1, compu2] 

        return players


class Statistics():

    @staticmethod
    def node_count_alpha_beta(game_n:int, width:int, height:int, depth:int) -> Tuple[int, int]:
        """counts the nodes visited for move 1.

        Args:
            game_n (int): game n
            width (int): width
            height (int): height
            depth (int): depth

        Returns:
            Tuple[int, int]: nodes visited, pruned branches
        """

        players = App._get_alpha_beta(game_n, depth)
        game = Game(game_n, width, height, players)
        game_iter = game.play_by_move()
        next(game_iter) # returns initialized board
        _, _, current_player, _ = next(game_iter)
        return (
            players[(current_player+1) % 2].get_counter(),
            players[(current_player+1) % 2].get_prune_counter()
        )

    @staticmethod
    def node_count_min_max(game_n:int, width:int, height:int, depth:int) -> int:
        """counts the nodes visited for move 1.

        Args:
            game_n (int): game n
            width (int): width
            height (int): height
            depth (int): depth

        Returns:
            int: nodes visited
        """

        players = App._get_min_max(game_n, depth)
        game = Game(game_n, width, height, players)
        game_iter = game.play_by_move()
        next(game_iter) # returns initialized board
        _, _, current_player, _ = next(game_iter)
        return players[(current_player+1) % 2].get_counter()

    @staticmethod
    def simulate_alpha_beta(sizes:List[Tuple[int, int, int]], depth_range:List[int]) -> Dict[str, List[int]]:
        """plays one move for each size specified and puts result in a dictionary.

        Args:
            sizes (List[Tuple[int, int, int]]): first int := game_n
                                                second int := width of board
                                                third int := height of board
            depth_range (List[int]): the range of depth that want to be tested

        Returns:
            List[Dict[str, int]]: results. The tags are "width, height, depth, nodes, pruned"
        """
        r_lst = {
            'width'  : [],
            'height' : [],
            'depth'  : [],
            'nodes'  : [],
            'pruned' : []
        }
        for depth in depth_range:
            for game_n, width, height in sizes:
                nodes, prunes = Statistics.node_count_alpha_beta(game_n, width, height, depth)
                r_lst['width'].append(width)                
                r_lst['height'].append(height)
                r_lst['depth'].append(depth)
                r_lst['nodes'].append(nodes)
                r_lst['pruned'].append(prunes)                
        return r_lst

    @staticmethod
    def simulate_min_max(sizes=List[Tuple[int, int, int]], depth_range=List[int]) -> Dict[str, List[int]]:
        """plays one move for each size specified and puts result in a dictionary.

        Args:
            sizes (List[Tuple[int, int, int]]): first int := game_n
                                                second int := width of board
                                                third int := height of board
            depth_range (List[int]): the range of depth that want to be tested

        Returns:
            List[Dict[str, int]]: results. The tags are "width, height, depth, nodes"
        """
        r_lst = {
            'width'  : [],
            'height' : [],
            'depth'  : [],
            'nodes'  : []
        }
        for depth in depth_range:
            for game_n, width, height in sizes:
                nodes = Statistics.node_count_min_max(game_n, width, height, depth)
                r_lst['width'].append(width)                
                r_lst['height'].append(height)
                r_lst['depth'].append(depth)
                r_lst['nodes'].append(nodes)
        return r_lst

    @staticmethod
    def visualize_alpha_beta(size:Tuple[int, int, int], depth_range:List[int]) -> None:
        """plots how many nodes alpha beta visits over diffrent depths

        Args:
            sizes (List[Tuple[int, int, int]]): first int := game_n
                                                second int := width of board
                                                third int := height of board
            depth_range (List[int]): List of depths to be plotted
        """
        d = Statistics.simulate_alpha_beta([size], depth_range)
        plt.plot(d['depth'], d['nodes'])
        plt.show()

    @staticmethod
    def visualize_compare(size:Tuple[int, int, int], depth_range:List[int]) -> None:
        """visualizes alpha-beta and min-max side by side for different depths

        Args:
            sizes (List[Tuple[int, int, int]]): first int := game_n
                                                second int := width of board
                                                third int := height of board
            depth_range (List[int]): range of depths to be plotted
        """
        d1 = Statistics.simulate_alpha_beta([size], depth_range)
        d2 = Statistics.simulate_min_max([size], depth_range)
        plt.plot(d1['depth'], d1['nodes'])
        plt.plot(d2['depth'], d2['nodes'])
        plt.ylabel('Nr. nodes Visited')
        plt.ylabel('depth')
        plt.show()

    @staticmethod
    def vizualize_compare_multiple_width(width_range:List[int], depth_range:List[int], game_n:int, height:int) -> None:
        """vizualizes the complexity of alpha-beta and min-max agents over different widths and depths

        Args:
            width_range (List[int]): range of widths to be plotted
            depth_range (List[int]): range of depths to be plotted
            game_n (int): gamen
            height (int): height (best plots if height is large)
        """
        
        f, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
        f.suptitle("Comparison for Different Widths", fontsize=13)
        
        for width in width_range:
            d = Statistics.simulate_alpha_beta([(game_n, width, height)], depth_range)
            ax1.plot(d['depth'], d['nodes'], label='width='+str(width))
        # labeling ax1
        ax1.set_title("Alpha Beta", fontsize=10)
        ax1.set_yscale('log')
        ax1.set_xticks(depth_range)

        for width in width_range:
            d = Statistics.simulate_min_max([(game_n, width, height)], depth_range)
            ax2.plot(d['depth'], d['nodes'])
        # labeling ax2
        ax2.set_title("Min-Max", fontsize=10)
        ax1.set_xticks(depth_range)

        # legend
        lines = []
        labels = []
        for ax in f.axes:
            axLine, axLabel = ax.get_legend_handles_labels()
            lines.extend(axLine)
            labels.extend(axLabel)

        f.legend(lines, labels, loc = 'upper right')
        f.text(0.5, 0.02, 'Depth', ha='center', fontsize=10)
        f.text(0.06, 0.5, 'Nr. Nodes Visited', va='center', fontsize=10, rotation='vertical')
        plt.show()

    @staticmethod
    def vizualize_compare_multiple_gamen(game_n_range:int, depth_range:List[int], width:int, height:int) -> None:
        """vizualizes the complexity of alpha-beta and min-max agents over different widths and depths

        Args:
            game_n_range (int): range of gamen to be plotted
            depth_range (List[int]): range of depths to be plotted
            width (int): width of board
            height (int): height of board
        """
        
        f, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
        f.suptitle("Comparison for Different Game N", fontsize=13)
        
        for game_n in game_n_range:
            d = Statistics.simulate_alpha_beta([(game_n, width, height)], depth_range)
            ax1.plot(d['depth'], d['nodes'], label='Game N='+str(game_n))
        # labeling ax1
        ax1.set_title("Alpha Beta", fontsize=10)
        ax1.set_yscale('log')
        ax1.set_xticks(depth_range)

        for game_n in game_n_range:
            d = Statistics.simulate_min_max([(game_n, width, height)], depth_range)
            ax2.plot(d['depth'], d['nodes'])
        # labeling ax2
        ax2.set_title("Min-Max", fontsize=10)
        ax1.set_yscale('log')
        ax1.set_xticks(depth_range)

        # legend
        lines = []
        labels = []
        for ax in f.axes:
            axLine, axLabel = ax.get_legend_handles_labels()
            lines.extend(axLine)
            labels.extend(axLabel)

        f.legend(lines, labels, loc = 'upper right')
        f.text(0.5, 0.02, 'Depth', ha='center', fontsize=10)
        f.text(0.06, 0.5, 'Nr. Nodes Visited', va='center', fontsize=10, rotation='vertical')
        plt.show()

    @staticmethod
    def vizualize_node_count_over_time(game_n:int, depth:int, width:int, height:int) -> None:
        """simulates one game of min-max against alpha-beta and displays a plot of how many
           nodes where visited.

        Args:
            game_n (int): gamen
            depth (int): depth
            width (int): width
            height (int): height
        """

        mm = App._get_min_max(game_n, depth)[0]
        ab = App._get_alpha_beta(game_n, depth)[1]

        ab_nodes = []
        ab_x = []
        mm_nodes = []
        mm_x = []

        players = [mm, ab]
        game = Game(game_n, width, height, players)
        game_iter = game.play_by_move()
        next(game_iter) # returns initialized board
        move_nr = 0
        for board, _, current_player, _ in game_iter:
            move_nr += 1
            print(board)
            if current_player == 0:
                mm_nodes.append(players[(current_player+1) % 2].get_counter())
                mm_x.append(move_nr)
            else:
                ab_nodes.append(players[(current_player+1) % 2].get_counter())
                ab_x.append(move_nr)

        fig, ax = plt.subplots()
        fig.suptitle('Nodes visited over time')
        ax.plot(ab_x, ab_nodes, label='Min-Max')
        ax.plot(mm_x, mm_nodes, label='Alpha-beta')
        ax.set_xlabel('Move')
        ax.set_ylabel('Nr. of Nodes Visited')
        fig.legend()
        plt.show()