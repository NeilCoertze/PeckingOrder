# Used to test state generation for Pecking Order Game

import AllStatePermutations as ASP
import textdistance

state_permutations = ASP.AllStatePermutations()

# ---------------------------------------------------------

# Print all combinations of final states for both agents
all_final_states_both_agents = state_permutations.generate_all_final_states_both_agents()

state_permutations.all_final_states_both_agents_to_txt()

state_permutations.determine_scores()

state_permutations.all_pair_scores_to_txt()

state_permutations.generate_all_state_pair_payoffs()

state_permutations.all_state_pair_payoffs_to_txt()

list1 = [0,2,3,0]
list2 = [0,2,3,4]

print("Levenshtein Similarity")
print(textdistance.levenshtein.similarity(list1,list2))
print("Levenshtein Distance")
print(textdistance.levenshtein.distance(list1,list2))

# print("Pearson Correlation")
# print(state_permutations.get_pearson_correlation_coefficient(list1, list2))

