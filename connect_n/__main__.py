from connect_n.connectgame.app import App, Statistics

if __name__ == '__main__':
    # Play a game
    #App.launch()
    
    # Coplexity tests
    #Statistics.vizualize_compare_multiple_width([5,7,9,11], list(range(1, 8)), 4, 20)
    #Statistics.vizualize_node_count_over_time(game_n=5, depth=4, width=11, height=12)
    Statistics.vizualize_compare_multiple_gamen([3, 7, 10], [4], 13, 20)
