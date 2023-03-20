# This class is used to instantiate and play games of pecking order

import Agents.RandomAgent as RA
import Agents.LevenshteinAgent as LA
import Agents.ZeroOrderAgent as ZOA
import Agents.FixedActionAgent as FAA
import PeckingOrderGame as POG

# # Instantiate the Pecking Order Game
PeckingOrderGame = POG.PeckingOrderGame()

# # Instantiate the Agents
AgentOne = ZOA.ZeroOrderAgent()
# AgentTwo = FAA.FixedActionAgent() 
AgentTwo = ZOA.ZeroOrderAgent()

# # Initialize the agents
AgentOne.init_agent(1, 0.5) # (params: agent_number, learning_rate)
AgentTwo.init_agent(2, 0.05)

# Initialize the Pecking Order Game
PeckingOrderGame.init_game(AgentOne, AgentTwo, "sequential")

# Play the Pecking Order Game
# PeckingOrderGame.play_full_game_displayed()

# Play multiple games and check number of wins

x = 100
print("Playing {} Games:".format(x))
print("ZERO-ORDER INITIAL BELIEFS: ", AgentOne.get_current_beliefs_rounded())
win_count = PeckingOrderGame.play_x_games(x)
print("Player 1 ({}) Wins: {} ({}%)\nPlayer 2 ({}) Wins: {} ({}%)\nDraws: {} ({}%)".format(AgentOne.get_agent_type(), win_count[0], float(100*(win_count[0])/float(x)), AgentTwo.get_agent_type(), win_count[1], 100*(float(win_count[1])/float(x)), win_count[2], 100*(float(win_count[2])/float(x))))

# After learning, play one fully displayed game to view the agents in action
print("\n\n\n\n\n============ FULL GAME BELOW =========\n") 
PeckingOrderGame.reset_game()
print("ZERO-ORDER CURRENT BELIEFS: ", AgentOne.get_current_beliefs_rounded())
PeckingOrderGame.play_full_game_displayed()

# Play multiple multiple games (used to determine general trends)
    # 'x' represents the number of rounds to play per game, and 'n'
    # represents the number of games to play.
# x = 50
# n = 5
# total_wins_one = 0
# total_wins_two = 0
# total_draws = 0
# for i in range(0, n):
#     print("Game batch: ", i)
#     # win_count = PeckingOrderGame.play_x_games("sequential", x)
#     win_count = PeckingOrderGame.play_x_games("sequential", x) # TODO: investigate why this always gives player 1 100% win rate
#     if win_count[0] > win_count[1]:
#         total_wins_one += 1
#     elif win_count[0] < win_count[1]:
#         total_wins_two += 1
#     elif win_count[0] == win_count[1]:
#         total_draws += 1
# print("(Player 1 Wins: {} ({}%), Player 2 Wins: {} ({}%), Draws: {} ({}%))".format(total_wins_one, float(100*(total_wins_one)/float(n)), total_wins_two, 100*(float(total_wins_two)/float(n)), total_draws, 100*(float(total_draws)/float(n))))
