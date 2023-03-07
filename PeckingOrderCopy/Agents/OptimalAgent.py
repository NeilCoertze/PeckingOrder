# Class used to define the setup of the zero-order Theory of Mind agent

import random
from Agents import SimpleAgent
import numpy as np
from scipy.stats import pearsonr
import textdistance

class OptimalAgent(SimpleAgent.SimpleAgent):
    def __init__(self):
        SimpleAgent.SimpleAgent.__init__(self)
        self.state_pair_payoffs = []

    # Initialize the state of a newly created agent
    def init_agent(self, player_number):
        SimpleAgent.SimpleAgent.init_agent(self, player_number)
        self.init_state_pair_payoffs()
    
    # Initialize the optimal agents knowledge about all possible payoffs
    def init_state_pair_payoffs(self):
        # opening the file in read mode
        my_file = open("all_state_pair_payoffs.txt", "r")
        
        # reading the file
        data = my_file.read()
        
        # replacing end splitting the text when newline ('\n') is seen.
        imported_payoffs = data.split("\n")
    
        lst_tuples = [eval(s) for s in imported_payoffs]

        self.state_pair_payoffs = lst_tuples.copy()
        my_file.close() 

    # Get the agents state pair payoffs
    def get_state_pair_payoffs(self):
        return self.state_pair_payoffs

    def get_levenshtein_similarity(self, list1, list2):
        return textdistance.levenshtein.similarity(list1,list2)

    # Pearson Correlation Coefficient
    def get_pearson_correlation_coefficient(self, array_one, array_two):
        np_array_one = np.array(array_one)
        np_array_two = np.array(array_two)

        np_array_one = [0 if x is None else x for x in np_array_one]
        np_array_two = [0 if x is None else x for x in np_array_two]

        corr_coeff, _ = pearsonr(np_array_one, np_array_two)
        return corr_coeff

    # Get a list of the most similar board states
    def get_most_similar_board_states(self):
        current_index = 0
        # most_similar_index = 0
        highest_sim_val_agent_board = 0
        highest_sim_val_opponent_board = 0
        most_similar_successor_states = []
        # For every payoff pair, determine which state is the most similar to the one 
        # being viewed by the agent based on the sum of similarity of their own board
        # state and the opponents board state to those in the list of payoff pairs. 
        for payoff_pair in self.state_pair_payoffs:
            # Agents Board State
            #sim_agent_pair = self.get_pearson_correlation_coefficient(payoff_pair[0], self.perches)
            sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
            # Opponents Board State
            #sim_opp_pair = self.get_pearson_correlation_coefficient(payoff_pair[1], self.perches_opponent)
            sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches_opponent)
            # Compare similarities of currently best states
            if((sim_agent_pair + sim_opp_pair) > (highest_sim_val_agent_board + highest_sim_val_opponent_board)):
                highest_sim_val_agent_board = sim_agent_pair
                highest_sim_val_opponent_board = sim_opp_pair
                # most_similar_index = current_index
            current_index += 1
        current_index = 0
        # Now compile a list of all the most similar board states
        for payoff_pair in self.state_pair_payoffs:
            # Agents Board State
            sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
            # Opponents Board State
            sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches_opponent)
            # Add all states with the same highest similarity to a list 
            if((sim_agent_pair + sim_opp_pair) == (highest_sim_val_agent_board + highest_sim_val_opponent_board)):
                most_similar_successor_states.append(self.state_pair_payoffs[current_index])
            current_index += 1
        return most_similar_successor_states

    # Determine the optimal action based on the cards the agent still has left 
    # Return both card and (unoccupied) perch
    # Determine all the winning states the agent can reach from this 
    def get_optimal_winning_states(self):
        # Get list of most similar states
        most_similar_states = self.get_most_similar_board_states()
        state_index = 0
        winning_states = []
        highest_value_winning_state = 0
        for payoff_pair in most_similar_states:
            # Determine winner in payoff pair
            winner_of_game = payoff_pair[2][0]
            agent_score = 0
            opponent_score = 0
            # Determine overall scores
            if self.player_number == 1:
                agent_score = payoff_pair[2][1]
                opponent_score = payoff_pair[2][2]
            elif self.player_number == 2:
                agent_score = payoff_pair[2][2]
                opponent_score = payoff_pair[2][1]
            # If agent wins the game in state, add to list of winning states
            if winner_of_game == self.player_number:
                # print(most_similar_states[state_index])
                # print("Player Number {}, Agent Score {}, Opponent Score {}".format(self.player_number, agent_score, opponent_score))
        
                winning_states.append(most_similar_states[state_index])
                if agent_score > highest_value_winning_state:
                    highest_value_winning_state = agent_score
            state_index += 1

        # Determine the states with the highest payoffs and append to list
        best_winning_states = []
        for winning_state in winning_states:
            # print("Winning State:")
            # print(winning_state)
            if winning_state[2][self.player_number] == highest_value_winning_state:
                best_winning_states.append(winning_state)
        
        #-> print("Current State (self, opponent): {}".format(str(self.get_perch_state())))
        #print("Best Winning States")
        #print(best_winning_states)

        if len(best_winning_states) > 0:
            return best_winning_states
        else:
            return None

    # Return the most optimal action given the current state (card, perch) representation
    def get_optimal_action(self):
        # Get all optimal winning states
        winning_states = self.get_optimal_winning_states()
        # Keep track of best (card, perch) pair, along with levenshtein similarity
        best_card_perch_pair = (None, None)
        highest_levenhstein_similarity = 0
        # best_winning_state_index = 0
        # winning_state_index = 0

        # Play each card on every perch and keep track of the levenhtein similarity
        if winning_states != None:
            for winning_state in winning_states:
                #-> print("Winning state {}".format(str(winning_state)))
                #-> print("    - Player state {}".format(str(winning_state[self.player_number-1])))

                winning_player_state = winning_state[self.player_number-1]
                for perch_index in range(0, len(self.perches)):
                    #-> print("Checking perch index: {}".format(perch_index))
                    new_state = []
                    if(self.perches[perch_index] == None):
                        for card in self.cards:
                            if card != None and card not in self.perches and card in self.cards:
                                #-> print("Self.perches is: {}". format(self.perches))
                                new_state = self.perches.copy()
                                new_state[perch_index] = card
                                #-> print("New State is: {}".format(str(new_state)))
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                if levenhstein_similarity > highest_levenhstein_similarity:
                                    highest_levenhstein_similarity = levenhstein_similarity
                                    best_card_perch_pair = (card, perch_index)
                                    # winning_state_index = 
                                    #-> print("New best next state is {}, LevSim {}".format(str(new_state), highest_levenhstein_similarity))
            #= print("FUNC: get_optimal_action() START")
            #= print("Agent Number: {}, Perch State: {}".format(self.player_number,str(self.get_perch_state())))
            #= print("Best Action Pair: ", best_card_perch_pair)
            #= print("FUNC: get_optimal_action() END")
            return best_card_perch_pair
        else:
            # Take random action
            return None

    # Used for an agent to take an action (play a card on a perch and remove card from agents hand)
    # This agent uses the pearson correlation coefficient to determine the most optimal states
    # that it can reach given the cards it still has remaining
    def take_action(self):
        #= print("\n@@@@ BEFORE ACTION (Player {})".format(str(self.player_number)))
        # If no move has been made yet, play randomly
        if self.perches == [None, None, None, None] and self.perches_opponent == [None, None, None, None]:
            optimal_action = None
        else:
            # Determine optimal action
            optimal_action = self.get_optimal_action()
        if optimal_action != None and optimal_action != (None, None):
            #= print("OPTIMAL ACTION IS: ", optimal_action)
            self.perches[optimal_action[1]] = optimal_action[0]
            self.cards[optimal_action[0]-1] = None
        else: 
            #= if optimal_action == (None, None):
                #= print("********* NONE NONE OPTIMAL ACTION\n")
           #.. print("----------- Taking random action -------------")
            actionValid = False
            while(not actionValid):
                card_to_play = random.randint(1,4)
                perch_to_play = random.randint(1,4)
                if((self.cards[card_to_play-1] != None) and (self.perches[perch_to_play-1] == None)):
                    actionValid = True
                    self.perches[perch_to_play-1] = card_to_play
                    self.cards[card_to_play-1] = None

    # TODO delete later -> helper/debugging functions below 
    
    # Set the agents perches
    def set_both_perches(self, agent_perches, opponent_perches):
        self.perches = agent_perches
        self.perches_opponent = opponent_perches

                
