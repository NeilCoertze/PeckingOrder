'''
Class used to define the setup of the Levenshtein Agent. This agent generates all possible 
end-game state where both players have played all their cards using the Levenshtein similarity
metric. Following this, it evaluates the outcome of those end-game states, including the winner
of the game along with each players final score. More details are provided in the information
menu when running the model. 
'''

import sys, os
sys.path.append(os.getcwd())

import random
from Agents import RandomAgent
import textdistance

class LevenshteinAgent(RandomAgent.RandomAgent):
    def __init__(self):
        RandomAgent.RandomAgent.__init__(self)
        self.state_pair_payoffs = []            # A list of all end game board states for this agent and 
                                                # their opponent, along with the winner and final scores 

    # Initialize the state of a newly created agent
    def init_agent(self, player_number):
        RandomAgent.RandomAgent.init_agent(self, player_number)
        self.init_state_pair_payoffs()
        self.inverse_state_pair_payoffs()
        self.agent_type = "Levenshtein"
    
    # Initialize the Levenshtein agents knowledge about all possible payoffs
    def init_state_pair_payoffs(self):
        # Open the file in read mode
        my_file = open("all_state_pair_payoffs.txt", "r")
        # Read the file
        data = my_file.read()
        # Replace ans plit text when newline ('\n') is encountered
        imported_payoffs = data.split("\n")
        lst_tuples = [eval(s) for s in imported_payoffs]
        self.state_pair_payoffs = lst_tuples.copy()
        my_file.close() 

    # Get the agents state pair payoffs
    def get_state_pair_payoffs(self):
        return self.state_pair_payoffs

    def get_levenshtein_similarity(self, list1, list2):
        return textdistance.levenshtein.similarity(list1,list2)

    # Get a list of the most similar board states to the current board state
    def get_most_similar_board_states(self):
        current_index = 0
        highest_sim_val_agent_board = -1
        highest_sim_val_opponent_board = -1
        sim_agent_pair = 0
        sim_opp_pair = 0
        most_similar_successor_states = []
        # For every payoff pair in the list of payoff pairs, determine which state is 
        # the most similar to the one being viewed by the agent based on the sum of the
        # similarity of their own board state and the opponents board state. 
        for payoff_pair in self.state_pair_payoffs:
            if self.player_number == 1:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches_opponent) 
            if self.player_number == 2:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches_opponent)
            # Find the greatest similarity values among all states
            if((sim_agent_pair + sim_opp_pair) >= (highest_sim_val_agent_board + highest_sim_val_opponent_board)):
                highest_sim_val_agent_board = sim_agent_pair
                highest_sim_val_opponent_board = sim_opp_pair
            current_index += 1
        current_index = 0
        # Now compile a list of all the most similar board states (using the 'highest similarity' value)
        for payoff_pair in self.state_pair_payoffs:
            if self.player_number == 1:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches_opponent)
            if self.player_number == 2:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches_opponent)
            # Add all states with the same highest similarity to a list
            if((sim_agent_pair + sim_opp_pair) >= ((highest_sim_val_agent_board + highest_sim_val_opponent_board))):
                most_similar_successor_states.append(self.state_pair_payoffs[current_index])
            current_index += 1
        return most_similar_successor_states

    # Determine all the winning states the agent can reach from the current board state
    def get_best_winning_states(self):
        # Get list of most similar states
        most_similar_states = self.get_most_similar_board_states()
        state_index = 0
        winning_states = []
        tied_states = []
        highest_value_winning_state = 0
        for payoff_pair in most_similar_states:
            # Determine winner in payoff pair
            winner_of_game = payoff_pair[2][0]
            agent_score = 0
            # Determine overall scores
            if self.player_number == 1:
                agent_score = payoff_pair[2][1]
            elif self.player_number == 2:
                agent_score = payoff_pair[2][2]
            # If agent wins the game in state, add to list of winning states
            if winner_of_game == self.player_number:
                winning_states.append(most_similar_states[state_index])
                if agent_score > highest_value_winning_state:
                    highest_value_winning_state = agent_score
            # If agent ties the game, add to list of tied states
            if winner_of_game == 0:
                tied_states.append(most_similar_states[state_index])
            state_index += 1
        # Determine the states with the highest payoffs and append to list
        best_winning_states = []
        for winning_state in winning_states:
            if winning_state[2][self.player_number] == highest_value_winning_state:
                best_winning_states.append(winning_state)
        if len(best_winning_states) > 0:
            return best_winning_states
        elif len(best_winning_states) == 0 and len(tied_states) > 0:
            return tied_states
        else:
            return None

    # Return one of the best actions given the current board state in (card, perch) representation
    def get_best_action(self):
        # Get all best winning states
        winning_states = self.get_best_winning_states()
        # Keep track of best (card, perch) pairs, along with levenshtein similarity
        best_card_perch_pairs = []
        highest_levenhstein_similarity = 0
        # Play each card on every perch and keep track of the levenhtein similarity
        if winning_states != None:
            for winning_state in winning_states:
                winning_player_state = winning_state[self.player_number-1]
                for perch_index in range(0, len(self.perches)):
                    new_state = []
                    # If a valid card can be played on a particular perch, create a new state and compare it with the current winning state
                    if(self.perches[perch_index] == None):
                        for card in self.cards:
                            if card != None and card not in self.perches and card in self.cards:
                                new_state = self.perches.copy()
                                new_state[perch_index] = card
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                # Find the highest Levenshtein similarity to a winning state
                                if levenhstein_similarity >= highest_levenhstein_similarity:
                                    highest_levenhstein_similarity = levenhstein_similarity
                        # Get the best (card, perch) pairs
                        for card in self.cards:
                            if card != None and card not in self.perches and card in self.cards:
                                new_state = self.perches.copy()
                                new_state[perch_index] = card
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                # If a high Levenshtein similarity compared to a winning state is found, add the (card, perch) pair to a list of 'good' actions
                                if levenhstein_similarity >= highest_levenhstein_similarity:
                                    best_card_perch_pairs.append((card, perch_index))
                # Since we have multiple 'good' actions, we choose one of the good actions at random
                if len(best_card_perch_pairs) > 0:
                    return random.choice(best_card_perch_pairs)
                else:
                # If none of the agent actions seem to lead to a winning state, take a random action
                    return (None, None)
        else:
            # If none of the agent actions seem to lead to a winning state, take a random action
            return None

    # Used by an agent to take an action (play a card on a perch and remove card from agents hand)
    def take_action(self):
        # Determine best action
        best_action = self.get_best_action()
        if best_action != None and best_action != (None, None):
            self.perches[best_action[1]] = best_action[0]
            # Remove card from hand
            self.cards[best_action[0]-1] = None
        else:
            if None in self.cards:
                # Take Random Action
                actionValid = False
                while(not actionValid):
                    card_to_play = random.randint(1,4)
                    perch_to_play = random.randint(1,4)
                    if((self.cards[card_to_play-1] != None) and (self.perches[perch_to_play-1] == None)):
                        actionValid = True
                        self.perches[perch_to_play-1] = card_to_play
                        self.cards[card_to_play-1] = None

    # Helper Function: create inverse of state_pair_payoffs for agent to use
    # This permutes all possible end-states, such that the agent can consider
    # all outcomes regardless of if he is player 1 or player 2.
    def inverse_state_pair_payoffs(self):        
        inverse_state_pair_payoffs = []
        for state_pair_payoff in self.state_pair_payoffs:
            player_one_board = state_pair_payoff[0]
            player_two_board = state_pair_payoff[1]
            final_score = state_pair_payoff[2]
            # Here we create new tuples and append to self.state_pair_payoffs
            inverse_player = 0
            inverse_player_one_score = final_score[2]
            inverse_player_two_score = final_score[1]
            if final_score[0] == 1:
                inverse_player = 2
            elif final_score[0] == 2:
                inverse_player = 1
            else:
                inverse_player = 0
            inverse_final_score = (inverse_player, inverse_player_one_score, inverse_player_two_score)
            inverse_state_pair_payoffs.append((player_two_board, player_one_board, inverse_final_score))
        for final_state in inverse_state_pair_payoffs:
            self.state_pair_payoffs.append(final_state)
