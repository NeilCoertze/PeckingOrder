# Class used to test agents and their behavior

import ZeroOrderAgent as zoA
import OptimalAgent as OA

zoAgent = zoA.ZeroOrderAgent()

zoAgent.init_agent(1)

# print("Previous Beliefs")
# print(zoAgent.get_beliefs()[0])

# zoAgent.update_single_belief(1,1,8)

zoAgent.increase_belief_probability(1,1)
# print("Updated Beliefs")
# print(zoAgent.get_beliefs())

# print("Optimal Agent Initialization")

# optimalAgent = OA.OptimalAgent()
# optimalAgent.init_agent(1)
# # optimalAgent.get_state_pair_payoffs()

# optimalAgent.set_both_perches([0,4,0,None], [None,3,0,0])

# #print("Most Similar Board States Are")
# #print(optimalAgent.get_most_similar_board_states())

# optimalAgent.get_optimal_action()