# Class used to define the setup of the zero-order Theory of Mind agent

import random
import SimpleAgent
import textdistance
# from Agents import SimpleAgent

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

    # Get a list of the most similar board states
    def get_most_similar_board_states(self):
        current_index = 0
        highest_sim_val_agent_board = 0
        highest_sim_val_opponent_board = 0
        most_similar_successor_states = []
        # For every payoff pair, determine which state is the most similar to the one 
        # being viewed by the agent based on the sum of similarity of their own board
        # state and the opponents board state to those in the list of payoff pairs. 
        for payoff_pair in self.state_pair_payoffs:
            # Agents Board State
            sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
            # Opponents Board State
            sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches_opponent)
            # Compare similarities of currently best states
            if((sim_agent_pair + sim_opp_pair) > (highest_sim_val_agent_board + highest_sim_val_opponent_board)):
                highest_sim_val_agent_board = sim_agent_pair
                highest_sim_val_opponent_board = sim_opp_pair
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
            state_index += 1

        # Determine the states with the highest payoffs and append to list
        best_winning_states = []
        for winning_state in winning_states:
            if winning_state[2][self.player_number] == highest_value_winning_state:
                best_winning_states.append(winning_state)
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

        # Play each card on every perch and keep track of the levenhtein similarity
        if winning_states != None:
            for winning_state in winning_states:
                winning_player_state = winning_state[self.player_number-1]
                for perch_index in range(0, len(self.perches)):
                    new_state = []
                    if(self.perches[perch_index] == None):
                        for card in self.cards:
                            if card != None and card not in self.perches and card in self.cards:
                                new_state = self.perches.copy()
                                new_state[perch_index] = card
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                if levenhstein_similarity > highest_levenhstein_similarity:
                                    highest_levenhstein_similarity = levenhstein_similarity
                                    best_card_perch_pair = (card, perch_index)
            return best_card_perch_pair
        else:
            # Take random action
            return None

    # Used for an agent to take an action (play a card on a perch and remove card from agents hand)
    # This agent uses the pearson correlation coefficient to determine the most optimal states
    # that it can reach given the cards it still has remaining
    def take_action(self):
        # If no move has been made yet, play randomly (see 'else' below)
        if self.perches == [None, None, None, None] and self.perches_opponent == [None, None, None, None]:
            optimal_action = None # TODO: compile list of all winning states with highest possible score based on the first move
        else:
            # Determine optimal action
            optimal_action = self.get_optimal_action()
        if optimal_action != None and optimal_action != (None, None):
            self.perches[optimal_action[1]] = optimal_action[0]
            self.cards[optimal_action[0]-1] = None
        else: 
            # Take Random Action
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

                
