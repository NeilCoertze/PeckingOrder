# Class used to define the setup of the zero-order Theory of Mind agent
import sys, os
sys.path.append(os.getcwd())

import random
from Agents import LevenshteinAgent

class ZeroOrderAgent(LevenshteinAgent.LevenshteinAgent):
    def __init__(self):
        LevenshteinAgent.LevenshteinAgent.__init__(self)
        self.current_beliefs = []             # Beliefs the agent holds regarding the actions of his opponents in the current game
                                              # represented as pairs of (card, perch_location, belief_probability)
        self.overall_beliefs = []             # Beliefs the agent holds regarding the actions of his opponents over all games
                                              # represented as pairs of (card, perch_location, belief_probability)
        self.projected_opponent_perches = []  # A projection of the opponents perches based on Zero-Order ToM beliefs (0 = unknown)
        self.learning_rate = 0                # Learning rate of agent

    # Initialize the state of a newly created agent
    def init_agent(self, player_number, learning_rate):
        LevenshteinAgent.LevenshteinAgent.init_agent(self, player_number)
        self.init_beliefs()
        self.agent_type = "Zero-Order"
        self.projected_opponent_perches = self.perches_opponent.copy()
        self.inverse_state_pair_payoffs()
        self.learning_rate = learning_rate

    # Initialize Agents Beliefs about his opponents actions
    def init_beliefs(self):
        # If the agent has no prior beliefs over all games
        if len(self.overall_beliefs) == 0:
            # define the length of the array
            length = 16
            # generate an array of random numbers
            arr = [random.randint(0, 100) for _ in range(length)]
            # calculate the sum of the array
            total = sum(arr)
            # divide each element by the sum to get values that sum up to 1
            proportional_arr = [x/total for x in arr]
            iterator = 0
            for card_num in range(1, 5):
                for perch_num in range(1, 5):
                    # Initialize agents' initial beliefs to be random
                    self.overall_beliefs.append((card_num, perch_num, proportional_arr[iterator]))
                    iterator += 1
            belief_total = 0
            for i in range(0, len(self.overall_beliefs)):
                belief_total += self.overall_beliefs[i][2]
            self.current_beliefs = self.overall_beliefs.copy()

    # Resets the agents current beliefs
    def reset_current_beliefs(self):
        # If overall beliefs are not none, set current beliefs to overall beliefs
        if len(self.overall_beliefs) > 0:
            self.current_beliefs = self.overall_beliefs.copy()
        else:
            self.init_beliefs()

    # Reset the agent
    def reset_agent(self):
        self.update_overall_beliefs()
        self.reset_current_beliefs()
        self.cards = [1, 2, 3, 4]
        self.perches = [None, None, None, None]
        self.perches_opponent = [None, None, None, None]

    # Update the overall beliefs of the agent once his opponent has played all of their cards
    def update_overall_beliefs(self):
        # For all opponent perches, increase belief probability based on cards played on perches
        for perch_index in range(0, len(self.perches_opponent)):
            self.increase_overall_belief_probability(self.perches_opponent[perch_index], perch_index+1)

    # Update belief probabilties by a particular value
    def increase_overall_belief_probability(self, card, perch): 
        # Calculate the sum of the belief probabilities
        total = 0
        iterator = 0
        belief_index = None
        beliefs_as_list = []
        for belief in self.overall_beliefs:
            total += belief[2]
            beliefs_as_list.append(belief[2])
            # Find the index of the belief to be adjusted
            if belief[0] == card and belief[1] == perch:
                belief_index = iterator
            iterator += 1
        # If an index is specified, increase the corresponding random number by 5%
        if belief_index is not None:
            beliefs_as_list[belief_index] += self.learning_rate
            total += self.learning_rate 
        # Calculate the probabilities by dividing each random number by the total
        new_belief_probabilities = [x / total for x in beliefs_as_list]
        # Assign new belief probabilities to self.overall_beliefs        
        for i in range(0, len(self.overall_beliefs)):
            self.overall_beliefs[i] = (self.overall_beliefs[i][0], self.overall_beliefs[i][1], new_belief_probabilities[i])

    # Calculate proportional probability assigned to each belief of the agent
    def calculate_belief_proportionality(self):
        # Calculate the sum of the belief probabilities
        total = 0
        beliefs_as_list = []
        for belief in self.current_beliefs:
            total += belief[2]
            beliefs_as_list.append(belief[2])
        # If there are still actions that can be taken
        if total > 0:
            # Calculate the probabilities by dividing each random number by the total
            new_belief_probabilities = [x / total for x in beliefs_as_list]
            # Assign new belief probabilities to self.current_beliefs        
            for i in range(0, len(self.current_beliefs)):
                self.current_beliefs[i] = (self.current_beliefs[i][0], self.current_beliefs[i][0], new_belief_probabilities[i])

    # Get current beliefs of agent
    def get_current_beliefs(self):
        return self.current_beliefs

    # Get current rounded beliefs of agent
    def get_current_beliefs_rounded(self):
        rounded_beliefs = []
        for belief in self.current_beliefs:
            rounded_belief = (belief[0], belief[1], round(belief[2], 3))
            rounded_beliefs.append(rounded_belief)
        return rounded_beliefs
    
    # Get overall beliefs of agent
    def get_overall_beliefs(self):
        return self.overall_beliefs
    
    # Get current rounded beliefs of agent
    def get_overall_beliefs_rounded(self):
        rounded_beliefs = []
        for belief in self.overall_beliefs:
            rounded_belief = (belief[0], belief[1], round(belief[2], 2))
            rounded_beliefs.append(rounded_belief)
        return rounded_beliefs

    # Update Belief Value for specific card on specific perch
    def update_single_current_belief(self, card_num, perch_num, belief_value):
        for index in range(0, len(self.current_beliefs)):
            if (self.current_beliefs[index][0] == card_num) and (self.current_beliefs[index][1] == perch_num):
                new_belief = list(self.current_beliefs[index])
                new_belief[2] = belief_value
                self.current_beliefs[index] = tuple(new_belief)

    # Update the beliefs of the agent
    def update_current_beliefs(self):
        # Check which cards have already been played by the opponent
        # If any perches are occupied, set beliefs about (card, perch, belief) to zero, since no 
        # other cards can be played on that particular perch
        for card_perch_pair in self.current_beliefs:
            for perch_index in range(0, len(self.perches_opponent)):
                # Update all card belief values based on opponent perches
                if card_perch_pair[0] == self.perches_opponent[perch_index]:
                    self.update_single_current_belief(card_perch_pair[0], perch_index, 0)
                # Update all perch belief values based on opponent cards on perches
                if self.perches_opponent[perch_index] != None and self.perches_opponent[perch_index] != 0:
                    self.update_single_current_belief(card_perch_pair[0], perch_index, 0)
        # Recalculate proportional belief values (in practice makes no difference, but theoretically more neat)
        self.calculate_belief_proportionality()

    # Get most probable action opponent will take based on agents current beliefs
    def get_highest_current_belief_opponent_action(self):
        # If the opponent can no longer take any actions (i.e. all actions already taken)
        if None not in self.perches_opponent:   
            return None
        else:
            highest_current_belief_index = 0
            highest_current_belief_value = 0
            for index in range(0, len(self.current_beliefs)):
                if self.current_beliefs[index][2] > highest_current_belief_value:
                    highest_current_belief_index = index
                    highest_current_belief_value = self.current_beliefs[index][2]
            return self.current_beliefs[highest_current_belief_index]

    # Project the cards on the opponents perches based on agent beliefs
    # Note: The Zero-Order ToM agent projects one action/step into the future
    def project_perches_opponent(self):
        
        # Determine the most probable action the opponent will take based on beliefs
        highest_belief_opponent_action = self.get_highest_current_belief_opponent_action()
        self.projected_opponent_perches = self.perches_opponent.copy()
        # If the opponent still has one action left to play
        if highest_belief_opponent_action != None:
            projected_card = highest_belief_opponent_action[0]
            projected_perch = highest_belief_opponent_action[1]
            self.projected_opponent_perches[projected_perch-1] = projected_card
            # Predict the most likely upside-down cards on the board
            predicted_upside_down_cards = self.predict_upside_down_cards()
            for index in range(0, len(predicted_upside_down_cards)):
                if predicted_upside_down_cards[index] != None and self.projected_opponent_perches[index] == 0:
                    self.projected_opponent_perches[index] = predicted_upside_down_cards[index]
        else: 
            # If the opponent has taken all actions possible, projected perches
            # is equivalent to the current opponents perches
            self.projected_opponent_perches = self.perches_opponent
            # Predict the most likely upside-down cards on the board
            predicted_upside_down_cards = self.predict_upside_down_cards()
            for index in range(0, len(predicted_upside_down_cards)):
                if predicted_upside_down_cards[index] != None and self.projected_opponent_perches[index] == 0:
                    self.projected_opponent_perches[index] = predicted_upside_down_cards[index]

    # Predicts which upside-down cards are most likely already on the board based on beliefs
    def predict_upside_down_cards(self):
        # For each upside down card currently in the opponents perches, assign most likely value
        most_likely_cards = [None, None, None, None]
        for perch_index in range(0, len(self.perches_opponent)):
            most_likely_card = 0
            highest_belief_value = 0
            # If an upside-down card is on this perch, find most likely card based on belief value
            if self.perches_opponent[perch_index] == 0:
                for belief in self.current_beliefs:
                    if belief[1] == perch_index+1:
                        # TODO: check the 'check' below
                        if belief[2] >= highest_belief_value and belief[0] not in self.perches_opponent:
                            most_likely_card = belief[0]
                        most_likely_cards[perch_index] = most_likely_card
        return most_likely_cards

    # Get a list of the most similar board states
    def get_most_similar_board_states(self):
        current_index = 0
        highest_sim_val_agent_board = -1
        highest_sim_val_opponent_board = -1
        sim_agent_pair = 0
        sim_opp_pair = 0
        most_similar_successor_states = []
        self.project_perches_opponent()
        # For every payoff pair, determine which state is the most similar to the one 
        # being viewed by the agent based on the sum of similarity of their own board
        # state and the opponents board state to those in the list of payoff pairs.
        # This gives us a 'highest similarity' value which we can use later
        for payoff_pair in self.state_pair_payoffs:
            if self.player_number == 1:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.projected_opponent_perches)
            if self.player_number == 2:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.projected_opponent_perches)
            # Find the greatest similarity values among all states
            if((sim_agent_pair + sim_opp_pair) >= (highest_sim_val_agent_board + highest_sim_val_opponent_board)):
                highest_sim_val_agent_board = sim_agent_pair
                highest_sim_val_opponent_board = sim_opp_pair
            current_index += 1
        current_index = 0
        # Now compile a list of all the most similar board states (using our 'highest similarity' value)
        for payoff_pair in self.state_pair_payoffs:
            if self.player_number == 1:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.projected_opponent_perches)
            if self.player_number == 2:
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.projected_opponent_perches)
            # Add all states with the same highest similarity to a list
            if((sim_agent_pair + sim_opp_pair) >= ((highest_sim_val_agent_board + highest_sim_val_opponent_board))):
                most_similar_successor_states.append(self.state_pair_payoffs[current_index])
            current_index += 1
        return most_similar_successor_states

    # Determine the best action based on the cards the agent still has left 
    # Return both card and (unoccupied) perch values
    # Determine all the winning states the agent can reach 
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

    # Return the most best action given the current state (card, perch) representation
    def get_best_action(self):
        # Get all best winning states
        winning_states = self.get_best_winning_states()
        # Keep track of best (card, perch) pair, along with levenshtein similarity
        best_card_perch_pairs = [] # (None, None)
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
                                if levenhstein_similarity >= highest_levenhstein_similarity:
                                    highest_levenhstein_similarity = levenhstein_similarity
                        # Get the best (card, perch) pair
                        for card in self.cards:
                            if card != None and card not in self.perches and card in self.cards:
                                new_state = self.perches.copy()
                                new_state[perch_index] = card
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                if levenhstein_similarity >= highest_levenhstein_similarity:
                                    best_card_perch_pairs.append((card, perch_index))
                if len(best_card_perch_pairs) > 0:
                    return random.choice(best_card_perch_pairs)
                else:
                    return (None, None)
        else:
            # Take random action
            return None

    # Used for an agent to take an action (play a card on a perch and remove card from agents hand)
    # First the agent considers his beliefs about what his opponent will play. The agent projects the
    # game one move into the future (i.e. 'if my opponent has played (oc, op), I should play (ac, ap)')
    # Moreover, the agent uses his current beliefs to predict what the values of upside-down cards are 
    # on the board. The agent then uses the Levenshtein similarity to select the best action he can take given the 
    # projected state. 
    def take_action(self):
        # Play according to beliefs
        # If no projected state exists (i.e. only one card left to play), then:
        # Determine best action
        best_action = self.get_best_action()
        if best_action != None and best_action != (None, None):
            self.perches[best_action[1]] = best_action[0]
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

        # Append
        for final_state in inverse_state_pair_payoffs:
            self.state_pair_payoffs.append(final_state)
            
