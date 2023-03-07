# Produce all the permutations possible in a game of Pecking Order
import itertools
import numpy as np
from scipy.stats import pearsonr

class AllStatePermutations:
    def __init__(self):
        self.all_final_states = []
        self.all_final_states_both = []
        self.all_pair_scores = []
        self.all_state_pair_payoffs = []
    
    # Generate all possible final states for a single agent
    def generate_all_final_states_single_agent(self):
        to_permute = [1, 2, 3, 4]
        all_states = itertools.permutations(to_permute, 4)
        for state in all_states:
            self.all_final_states.append(state)
            print(state)

    # Generate all combinations of possible final states for a both agents
    def generate_all_final_states_both_agents(self):
        to_permute = [1, 2, 3, 4]
        all_states = itertools.permutations(to_permute, 4)
        for state in all_states:
            self.all_final_states.append(state)

        to_permute_all = self.all_final_states
        permuted_all = itertools.combinations_with_replacement(to_permute_all, 2)
        # print(to_permute_all_final)
        for double_state in permuted_all:
            self.all_final_states_both.append(double_state)
    
        return self.all_final_states_both
        
    # Display all possible states for a single agent
    def show_all_final_states_single_agent(self):
        print(self.all_final_states)

    # Write all states to .txt file
    def all_final_states_single_agent_to_txt(self):
        with open('all_final_states_single_agent.txt', 'w') as fp:
            for state in self.all_final_states:
                # write each item on a new line
                fp.write("%s\n" % str(state))

    # Write all double states to .txt file
    def all_final_states_both_agents_to_txt(self):
        with open('all_final_states_both_agents.txt', 'w') as fp:
            for state in self.all_final_states_both:
                # write each item on a new line
                fp.write("%s\n" % str(state))

    # Return the winner of the game along with their score (return: 1 for agent one, 2 for agent two)
    def determine_scores(self):        
        pair_scores = []
        for pair_num in range(0, len(self.all_final_states_both)):
            agent_one_score = 0
            agent_two_score = 0
            # Lowest Value Perch (1 point)
            if self.all_final_states_both[pair_num][0][0] > self.all_final_states_both[pair_num][1][0]:
                agent_one_score += 1
            elif self.all_final_states_both[pair_num][0][0] < self.all_final_states_both[pair_num][1][0]:
                agent_two_score += 1
            
            # Second-Lowest Value Perch (2 points)
            if self.all_final_states_both[pair_num][0][1] > self.all_final_states_both[pair_num][1][1]:
                agent_one_score += 2
            elif self.all_final_states_both[pair_num][0][1] < self.all_final_states_both[pair_num][1][1]:
                agent_two_score += 2

            # Second-Highest Value Perch (3 points)
            if self.all_final_states_both[pair_num][0][2] > self.all_final_states_both[pair_num][1][2]:
                agent_one_score += 3
            elif self.all_final_states_both[pair_num][0][2] < self.all_final_states_both[pair_num][1][2]:
                agent_two_score += 3

            # Highest Value Perch (4 points)
            if self.all_final_states_both[pair_num][0][3] > self.all_final_states_both[pair_num][1][3]:
                agent_one_score += 4
            elif self.all_final_states_both[pair_num][0][3] < self.all_final_states_both[pair_num][1][3]:
                agent_two_score += 4
            
            # Tie-Breaker
            if agent_one_score > agent_two_score:
                # Agent one wins
                pair_scores.append((1, agent_one_score, agent_two_score))
            elif agent_one_score < agent_two_score:
                # Agent two wins
                pair_scores.append((2, agent_one_score, agent_two_score))
            elif agent_one_score == agent_two_score:
                if self.all_final_states_both[pair_num][0][0] > self.all_final_states_both[pair_num][1][0]:
                    # Agent one wins
                    pair_scores.append((1, agent_one_score, agent_two_score))
                elif self.all_final_states_both[pair_num][0][0] < self.all_final_states_both[pair_num][1][0]:
                    # Agent two wins
                    pair_scores.append((2, agent_one_score, agent_two_score))
                elif self.all_final_states_both[pair_num][0][0] == self.all_final_states_both[pair_num][1][0]:
                    # Agents truly tied
                    pair_scores.append((0, agent_one_score, agent_two_score))

        self.all_pair_scores = pair_scores
    
    # Write all pair scores to .txt file
    def all_pair_scores_to_txt(self):
        with open('all_pair_scores.txt', 'w') as fp:
            for pair_score in self.all_pair_scores:
                # write each item on a new line
                fp.write("%s\n" % str(pair_score))

    def merge(self, list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, 300)]
        return merged_list

    # Generate all final state pairs and the payoff for each combination of states
    def generate_all_state_pair_payoffs(self):
        for i in range(0, len(self.all_final_states_both)):
            pair_and_payoff = list(self.all_final_states_both[i])
            pair_and_payoff.append(self.all_pair_scores[i])
            pair_and_payoff_tuple = tuple(pair_and_payoff)
            self.all_state_pair_payoffs.append(pair_and_payoff_tuple)
            # self.all_state_pair_payoffs.append(self.all_final_states_both[i] + (self.all_pair_scores[i])) 

    # Write all state pair payoffs to .txt file
    def all_state_pair_payoffs_to_txt(self):
        with open('all_state_pair_payoffs.txt', 'w') as fp:
            for state_pair_payoff in self.all_state_pair_payoffs:
                # write each item on a new line
                fp.write("%s\n" % str(state_pair_payoff))

    # Pearson Correlation Coefficient
    def get_pearson_correlation_coefficient(self, array_one, array_two):
        np_array_one = np.array(array_one)
        np_array_two = np.array(array_two)

        np_array_one = [np.nan if x is None else x for x in np_array_one]
        np_array_two = [np.nan if x is None else x for x in np_array_two]

        corr_coeff, _ = pearsonr(np_array_one, np_array_two)
        return corr_coeff