# This class is used to instantiate and play games of pecking order

import Agents.SimpleAgent as SA
import Agents.OptimalAgent as OA
import PeckingOrderGame as POG

# # Instantiate the Pecking Order Game
PeckingOrderGame = POG.PeckingOrderGame()

# # Instantiate the Agents
AgentOne =   SA.SimpleAgent() # OA.OptimalAgent() 
# AgentTwo = ZOA.ZeroOrderAgent()
AgentTwo =   OA.OptimalAgent() # SA.SimpleAgent()   

# # Initialize the agents
AgentOne.init_agent(1)
AgentTwo.init_agent(2)

# Initialize the Pecking Order Game
PeckingOrderGame.init_game(AgentOne, AgentTwo)

# Play the Pecking Order Game
# PeckingOrderGame.play_full_game_displayed("simultaneous")

# Play multiple games and check number of wins
x = 100
win_count = PeckingOrderGame.play_x_games("sequential", x)
print("(Player 1 Wins: {} ({}%), Player 2 Wins: {} ({}%), Draws: {} ({}%))".format(win_count[0], float(100*(win_count[0])/float(x)), win_count[1], 100*(float(win_count[1])/float(x)), win_count[2], 100*(float(win_count[2])/float(x))))

# # Play multiple multiple games (check if order of play matters)
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
