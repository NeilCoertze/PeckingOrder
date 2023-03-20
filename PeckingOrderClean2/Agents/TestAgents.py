# Class used to test agents and their behavior

import ZeroOrderAgent as zoA
import LevenshteinAgent as LA

# zoAgent = zoA.ZeroOrderAgent()

# zoAgent.init_agent(1)

# print("Previous Beliefs")
# print(zoAgent.get_beliefs())

# # zoAgent.update_single_belief(1,1,8)

# zoAgent.increase_belief_probability(1,1)
# print("Updated Beliefs")
# print(zoAgent.get_current_beliefs())

# print("Levenshtein Agent Initialization")

levenshteinAgent = LA.LevenshteinAgent()
levenshteinAgent.init_agent(1)
# levenshteinAgent.get_state_pair_payoffs()

# levenshteinAgent.set_both_perches([0,0,None,None], [1,2,None,None])
print("Similarity: ", levenshteinAgent.get_levenshtein_similarity([None,None,3,4], [2,1,3,4]))
#print("Most Similar Board States Are")
#print(levenshteinAgent.get_most_similar_board_states())

levenshteinAgent.get_best_action()