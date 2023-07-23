'''
Class used to define the setup of the First-Order Theory of Mind agent
'''

import sys, os
sys.path.append(os.getcwd())

import random
from Agents import LevenshteinAgent

class FirstOrderAgent(LevenshteinAgent.LevenshteinAgent): 
    def __init__(self):
        LevenshteinAgent.LevenshteinAgent.__init__(self)
        self.current_zero_order_beliefs = []                # Beliefs the agent holds regarding the actions of his opponents in the current game
                                                            # represented as pairs of (card, perch, belief value)
        self.overall_zero_order_beliefs = []                # Beliefs the agent holds regarding the actions of his opponents over all games
                                                            # represented as pairs of (card, perch, belief value)
        self.current_first_order_beliefs = []               # Beliefs the agent holds regarding what he thinks his opponent believes he will do
                                                            # in the current game (card, perch, belief value)
        self.overall_first_order_beliefs = []               # Beliefs the agent holds regarding what he thinks his opponent believes he will do
                                                            # over all games (card, perch, belief value)

        self.integrated_beliefs = []                        # Beliefs the agent holds regarding the actions of his opponents over all games
                                                            # based on integrated zero order beliefs and first order projections of the opponents 
                                                            # board state based on first order beliefs
        self.zero_order_projected_perches = []              # A projection of the opponents perches based on Zero-Order ToM beliefs (0 = unknown)
        self.previously_projected_first_order_perches = []  # Previously projected Zero Order Perches along with 
        self.perches_opponent_perspective = []              # This agents perches viewed from the perspective of the opponent
        self.first_order_projected_perches = []             # A projection of the opponents board state based on first order beliefs
        self.integrated_first_order_projected_perches = []  # A projection of the opponents board state based on integrated zero and first order beliefs
        self.opponent_zero_order_projected_perches = []     # The opponents projection of this agents perches based on this agents first order beliefs 
                                                            # (i.e. the opponents zero order beliefs)
        self.opponent_all_previous_best_actions = []        # All previous best (zero order) actions by the 'opponent' (i.e. what this agent believes his 
                                                            # (zero order) opponent projected the best actions would be)
        self.learning_rate = 0                              # Learning rate of agent
        self.first_order_confidence_level = 0               # Confidence level of agent regarding his first order ToM predictions of his opponents actions
        

    # Initialize the state of a newly created agent
    def init_agent(self, player_number, learning_rate, first_order_confidence_level):
        LevenshteinAgent.LevenshteinAgent.init_agent(self, player_number)
        self.init_zero_order_beliefs()
        self.init_first_order_beliefs()
        self.agent_type = "First-Order"
        self.zero_order_projected_perches = self.perches_opponent.copy()
        self.inverse_state_pair_payoffs()
        self.learning_rate = learning_rate 
        self.first_order_confidence_level = first_order_confidence_level

    # Initialize agents zero-order beliefs about his opponents actions
    def init_zero_order_beliefs(self):
        # If the agent has no prior beliefs over all games
        if len(self.overall_zero_order_beliefs) == 0:
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
                    # Initialize agents' initial zero-order beliefs to be random
                    self.overall_zero_order_beliefs.append((card_num, perch_num, proportional_arr[iterator]))
                    iterator += 1
            belief_total = 0
            for i in range(0, len(self.overall_zero_order_beliefs)):
                belief_total += self.overall_zero_order_beliefs[i][2]
            self.current_zero_order_beliefs = self.overall_zero_order_beliefs.copy()

    # Initialize agents first-order beliefs about what his opponent believes he will do 
    def init_first_order_beliefs(self):
        # Initialize first-order beliefs
        if len(self.overall_first_order_beliefs) == 0:
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
                    # Initialize agents initial first-order beliefs to be random
                    self.overall_first_order_beliefs.append((card_num, perch_num, proportional_arr[iterator]))
                    iterator += 1
            belief_total = 0
            for i in range(0, len(self.overall_first_order_beliefs)):
                belief_total += self.overall_first_order_beliefs[i][2]
            self.current_first_order_beliefs = self.overall_first_order_beliefs.copy()

    # Resets the agents current beliefs
    def reset_current_beliefs(self):
        # If overall beliefs are not none, set current beliefs to overall beliefs
        if len(self.overall_zero_order_beliefs) > 0:
            self.current_zero_order_beliefs = self.overall_zero_order_beliefs.copy()
        else:
            self.init_zero_order_beliefs()
        if len(self.overall_first_order_beliefs) > 0:
            self.current_first_order_beliefs = self.overall_first_order_beliefs.copy()
        else:
            self.init_first_order_beliefs()
    
    # Reset the agent
    def reset_agent(self):
        self.update_overall_beliefs("Zero-Order")
        self.update_overall_beliefs("First-Order")
        self.reset_current_beliefs()
        self.cards = [1, 2, 3, 4]
        self.perches = [None, None, None, None]
        self.perches_opponent = [None, None, None, None]
        self.zero_order_projected_perches = [None, None, None, None]
        self.opponent_all_previous_best_actions = []
        self.previously_projected_first_order_perches = []
        
    # Update overall zero order or first order beliefs
    def update_overall_beliefs(self, tom_order):
        # Check which order of ToM beliefs should be updated
        if tom_order == "Zero-Order":
            # For all opponent perches, increase zero order belief probability based on cards played on perches
            for perch_index in range(0, len(self.perches_opponent)):
                self.increase_overall_belief_probability(self.perches_opponent[perch_index], perch_index+1, "Zero-Order")
        elif tom_order == "First-Order":
            # For all of this agents own perches, increase first order beliefs probability based on cards played on perches
            for perch_index in range(0, len(self.perches)):
                self.increase_overall_belief_probability(self.perches[perch_index], perch_index+1, "First-Order")
        else:
            # If neither first or second order, there is a problem
            print("Error updating overall beliefs")

        # Update the overall first-order beliefs of the agent once he and his opponent have played all of their cards
    def update_overall_first_order_beliefs(self):
        # For all of this agents own perches, increase first order beliefs probability based on cards played on perches
        for perch_index in range(0, len(self.perches)):
            self.increase_overall_first_order_belief_probability(self.perches[perch_index], perch_index+1)

    # Update zero-order belief probabilties based on learning rate
    def increase_overall_belief_probability(self, card, perch, tom_order): 
        # Determine order of ToM
        overall_beliefs = []
        if tom_order == "Zero-Order":
            overall_beliefs = self.overall_zero_order_beliefs
        elif tom_order == "First-Order":
            overall_beliefs = self.overall_first_order_beliefs
        else: 
            print("Error increasing overall belief probability")
        # Calculate the sum of the belief probabilities
        total = 0
        iterator = 0
        belief_index = None
        beliefs_as_list = []
        for belief in overall_beliefs:
            total += belief[2]
            beliefs_as_list.append(belief[2])
            # Find the index of the belief to be adjusted
            if belief[0] == card and belief[1] == perch:
                belief_index = iterator
            iterator += 1
        # If an index is specified, increase the corresponding belief based on the learning rate
        if belief_index is not None:
            beliefs_as_list[belief_index] += self.learning_rate
            total += self.learning_rate 
        # Calculate the probabilities by dividing each new belief probability by the total
        new_belief_probabilities = [x / total for x in beliefs_as_list]
        # Assign new belief probabilities to overall zero-order beliefs        
        for i in range(0, len(overall_beliefs)):
            overall_beliefs[i] = (overall_beliefs[i][0], overall_beliefs[i][1], new_belief_probabilities[i])
    
    # Calculate proportional probability assigned to each zero-order belief of the agent
    def calculate_current_belief_proportionality(self, tom_order):
        # Determine order of ToM
        current_beliefs = []
        if tom_order == "Zero-Order":
            current_beliefs = self.current_zero_order_beliefs
        elif tom_order == "First-Order":
            current_beliefs = self.current_first_order_beliefs
        else: 
            print("Error calculating current belief proportionality")
        # Calculate the sum of the belief probabilities
        total = 0
        beliefs_as_list = []
        for belief in current_beliefs:
            total += belief[2]
            beliefs_as_list.append(belief[2])
        # If there are still actions that can be taken
        if total > 0:
            # Calculate the probabilities by dividing each random number by the total
            new_belief_probabilities = [x / total for x in beliefs_as_list]
            # Assign new belief probabilities to zero-order beliefs
            for i in range(0, len(current_beliefs)):
                current_beliefs[i] = (current_beliefs[i][0], current_beliefs[i][1], new_belief_probabilities[i])

    # Get current beliefs of agent
    def get_current_beliefs(self, tom_order, rounded = True):
        # Determine order of ToM and return rounded or non-rounded beliefs
        if tom_order == "Zero-Order" and rounded == True:
            rounded_beliefs = []
            for belief in self.current_zero_order_beliefs:
                rounded_belief = (belief[0], belief[1], round(belief[2], 3))
                rounded_beliefs.append(rounded_belief)
            return rounded_beliefs
        elif tom_order == "Zero-Order" and rounded == False:
            return self.current_zero_order_beliefs
        elif tom_order == "First-Order" and rounded == True:
            rounded_beliefs = []
            for belief in self.current_first_order_beliefs:
                rounded_belief = (belief[0], belief[1], round(belief[2], 3))
                rounded_beliefs.append(rounded_belief)
            return rounded_beliefs
        elif tom_order == "First-Order" and rounded == False:
            return self.current_first_order_beliefs
        elif tom_order == "First-Order-Integrated" and rounded == True:
            rounded_beliefs = []
            for belief in self.integrated_beliefs:
                rounded_belief = (belief[0], belief[1], round(belief[2], 3))
                rounded_beliefs.append(rounded_belief)
            return rounded_beliefs
        elif tom_order == "First-Order-Integrated" and rounded == False:
            return self.integrated_beliefs
        else: 
            print("Error calculating current belief proportionality")
        
        # Get overall beliefs of agent
    def get_overall_beliefs(self, tom_order, rounded = True):
        # Determine order of ToM and return rounded or non-rounded beliefs
        if tom_order == "Zero-Order" and rounded == True:
            rounded_beliefs = []
            for belief in self.overall_zero_order_beliefs:
                rounded_belief = (belief[0], belief[1], round(belief[2], 3))
                rounded_beliefs.append(rounded_belief)
            return rounded_beliefs
        elif tom_order == "Zero-Order" and rounded == False:
            return self.overall_zero_order_beliefs
        elif tom_order == "First-Order" and rounded == True:
            rounded_beliefs = []
            for belief in self.overall_first_order_beliefs:
                rounded_belief = (belief[0], belief[1], round(belief[2], 3))
                rounded_beliefs.append(rounded_belief)
            return rounded_beliefs
        elif tom_order == "First-Order" and rounded == False:
            return self.overall_first_order_beliefs
        else: 
            print("Error calculating overall belief proportionality")

    # Update belief value for specific card on specific perch
    def update_single_current_belief(self, card_num, perch_num, belief_value, tom_order):
        # Determine order of ToM
        current_beliefs = []
        if tom_order == "Zero-Order":
            current_beliefs = self.current_zero_order_beliefs
        elif tom_order == "First-Order":
            current_beliefs = self.current_first_order_beliefs
        else: 
            print("Error updating single current belief")
        # Update belief value
        for index in range(0, len(current_beliefs)):
            if (current_beliefs[index][0] == card_num) and (current_beliefs[index][1] == perch_num):
                new_belief = list(current_beliefs[index])
                new_belief[2] = belief_value
                current_beliefs[index] = tuple(new_belief)

    # Update the zero-order beliefs of the agent
    def update_current_zero_order_beliefs(self):
        # Check which cards have already been played by the opponent
        # If any perches are occupied, set beliefs about (card, perch, belief) to zero, since no 
        # other cards can be played on that particular perch
        for perch_index in range(0, len(self.perches_opponent)):
            for card_perch_pair in self.current_zero_order_beliefs:
                # If specific card is on opponent perch, update any beliefs including card 
                if self.perches_opponent[perch_index] != None and self.perches_opponent[perch_index] != 0 and self.perches_opponent[perch_index] == card_perch_pair[0]: 
                    self.update_single_current_belief(card_perch_pair[0], card_perch_pair[1], 0, "Zero-Order")
                # If specific perch is occupied, update any beliefs including that perch
                if self.perches_opponent[perch_index] != None and self.perches_opponent[perch_index] != 0 and perch_index+1 == card_perch_pair[1]:
                    self.update_single_current_belief(card_perch_pair[0], card_perch_pair[1], 0, "Zero-Order")
        # Recalculate proportional belief values (in practice makes no difference, but theoretically more neat)
        self.calculate_current_belief_proportionality("Zero-Order")

    # Get the opponents view of our perches
    def get_opponent_perspective_own_perches(self):
        self.perches_opponent_perspective = self.perches.copy()
        # Determine which of the agents perches the opponent has full view of, and which cards are upside down
        for index in range(0, len(self.perches)):
            if(self.perches[index] != None and self.perches_opponent[index] == None):
                self.perches_opponent_perspective[index] = 0

    # Update the first-order beliefs of the agent
    def update_current_first_order_beliefs(self):
        self.get_opponent_perspective_own_perches()
        for perch_index in range(0, len(self.perches)):
            for card_perch_pair in self.current_first_order_beliefs:
                # If specific card is on own perch and visible to opponent, update any beliefs including card
                if self.perches_opponent_perspective[perch_index] != None and self.perches_opponent_perspective[perch_index] != 0 and self.perches_opponent_perspective[perch_index] == card_perch_pair[0]: 
                    self.update_single_current_belief(card_perch_pair[0], card_perch_pair[1], 0, "First-Order")
                # If specific perch is occupied, update any beliefs including that perch
                if self.perches_opponent_perspective[perch_index] != None and self.perches_opponent_perspective[perch_index] != 0 and perch_index+1 == card_perch_pair[1]:
                    self.update_single_current_belief(card_perch_pair[0], card_perch_pair[1], 0, "First-Order")
        self.calculate_current_belief_proportionality("First-Order")

    # Get this agents highest current beliefs
    def get_highest_current_belief(self, tom_order):
        # Determine order of ToM
        current_beliefs = []
        if tom_order == "Zero-Order":
            current_beliefs = self.current_zero_order_beliefs
        elif tom_order == "First-Order":
            current_beliefs = self.current_first_order_beliefs
        elif tom_order == "First-Order-Integrated":
            current_beliefs = self.integrated_beliefs
        else: 
            print("Error getting highest current belief")
        # If the opponent can no longer take any actions (i.e. all actions already taken)
        if None not in self.perches_opponent:   
            return None
        else:
            # Return the highest current belief
            highest_current_belief_index = 0
            highest_current_belief_value = 0
            for index in range(0, len(current_beliefs)):
                if current_beliefs[index][2] > highest_current_belief_value:  
                    if tom_order == "Zero-Order" and self.perches_opponent[current_beliefs[index][1]-1] == None:
                        highest_current_belief_index = index
                        highest_current_belief_value = current_beliefs[index][2]
                    elif tom_order == "First-Order" and self.perches[current_beliefs[index][1]-1] == None:
                        highest_current_belief_index = index
                        highest_current_belief_value = current_beliefs[index][2]
                    elif tom_order == "First-Order-Integrated" and self.perches_opponent[current_beliefs[index][1]-1] == None:
                        highest_current_belief_index = index
                        highest_current_belief_value = current_beliefs[index][2]
            return current_beliefs[highest_current_belief_index]
    
    # Predict every upside down card the opponent has played based on zero order beliefs
    def predict_upside_down_cards_zero_order(self, highest_zero_order_belief):
        # For each upside down card currently in the opponents perches, assign most likely value
        most_likely_cards = [None, None, None, None]
        for perch_index in range(0, len(self.perches_opponent)):
            most_likely_card = None
            highest_belief_value = 0
            # If there is an upside down card in the opponents perches, check what the most likely card is to be played there. The
            # predicted upside down cards should not be the same as the the card this agent believes his opponent will play next turn 
            if self.perches_opponent[perch_index] == 0 and highest_zero_order_belief != None: 
                for belief in self.current_zero_order_beliefs:
                    if belief[1] == perch_index+1 and belief[2] >= highest_belief_value and belief[0] != highest_zero_order_belief[0]:
                        most_likely_card = belief[0]
                        highest_belief_value = belief[2]
                most_likely_cards[perch_index] = most_likely_card
        return most_likely_cards
    
    # Project the cards on the opponents perches based on this agents zero-order beliefs
    def project_perches_zero_order(self):
        # Determine the most probable action the opponent will take based on current zero-order beliefs
        highest_zero_order_belief = self.get_highest_current_belief("Zero-Order")
        self.zero_order_projected_perches = self.perches_opponent.copy()
        # If the opponent still has one action left to play
        if highest_zero_order_belief != None and highest_zero_order_belief != (None, None):
            projected_card = highest_zero_order_belief[0]
            projected_perch = highest_zero_order_belief[1]
            self.zero_order_projected_perches[projected_perch-1] = projected_card 
            # Predict the most likely upside-down cards on the board based on zero order beliefs
            predicted_upside_down_cards_zero_order = self.predict_upside_down_cards_zero_order(highest_zero_order_belief)
            for index in range(0, len(predicted_upside_down_cards_zero_order)):
                if predicted_upside_down_cards_zero_order[index] != None and self.zero_order_projected_perches[index] == 0:
                    self.zero_order_projected_perches[index] = predicted_upside_down_cards_zero_order[index]
        else: 
            # If the opponent has taken all actions possible, projected perches
            # is equivalent to the current opponents perches
            self.zero_order_projected_perches = self.perches_opponent.copy()
            # Predict the most likely upside-down cards on the board
            predicted_upside_down_cards = self.predict_upside_down_cards_zero_order(highest_zero_order_belief)
            for index in range(0, len(predicted_upside_down_cards)):
                if predicted_upside_down_cards[index] != None and self.zero_order_projected_perches[index] == 0:
                    self.zero_order_projected_perches[index] = predicted_upside_down_cards[index]

    # The opponents prediction of this agents upside down cards from their perspective
    def opponent_predict_upside_down_cards_zero_order(self, highest_first_order_belief):
        # For each upside down card currently in the opponents perches, assign most likely value
        most_likely_cards = [None, None, None, None]
        for perch_index in range(0, len(self.perches_opponent_perspective)):
            most_likely_card = None
            highest_belief_value = 0
            # If there is an upside down card in this agents perches, check what the most likely card is to be played there. The
            # predicted upside down cards should not be the same as the the card this agent believes his opponent believes he will
            # play next turn 
            if self.perches_opponent_perspective[perch_index] == 0 and highest_first_order_belief != None: 
                for belief in self.current_first_order_beliefs:
                    if belief[1] == perch_index+1 and belief[2] >= highest_belief_value and belief[0] != highest_first_order_belief[0]:
                        most_likely_card = belief[0]
                        highest_belief_value = belief[2]
                most_likely_cards[perch_index] = most_likely_card
        return most_likely_cards

    # Get the opponents projection of this agents perches
    def get_opponent_projection_zero_order(self):
        # Determine the most probable action the opponent will take based on current zero-order beliefs
        highest_first_order_belief = self.get_highest_current_belief("First-Order")
        self.get_opponent_perspective_own_perches()
        self.opponent_zero_order_projected_perches = self.perches_opponent_perspective
        # If the opponent still has one action left to play
        if highest_first_order_belief != None and highest_first_order_belief != (None, None):
            projected_card = highest_first_order_belief[0]
            projected_perch = highest_first_order_belief[1]
            self.opponent_zero_order_projected_perches[projected_perch-1] = projected_card 
        # Project this agents upside down cards based on first order beliefs and opponents view of this agents perches
        predicted_upside_down_cards = self.opponent_predict_upside_down_cards_zero_order(highest_first_order_belief)
        for index in range(0, len(predicted_upside_down_cards)):
            if predicted_upside_down_cards[index] != None and self.opponent_zero_order_projected_perches[index] == 0:
                self.opponent_zero_order_projected_perches[index] = predicted_upside_down_cards[index]
    
    # Predict the best cards the opponent could previouly have played based on first order beliefs
    def predict_upside_down_cards_first_order(self):
        for index in range(0, len(self.first_order_projected_perches)):
            if self.first_order_projected_perches[index] == 0:
                for card_perch_pair in self.opponent_all_previous_best_actions:
                    if card_perch_pair[1]-1 == index and card_perch_pair[0] not in self.first_order_projected_perches:
                        self.first_order_projected_perches[index] = card_perch_pair[0]

    # Project opponent perches based on first order beliefs
    def project_perches_first_order(self):
        self.first_order_projected_perches = self.perches_opponent.copy()
        # Get opponent projection of this agents perches based on first order beliefs
        self.get_opponent_projection_zero_order()
        # Get the best next action the opponent can take based on first order beliefs
        next_best_action = None
        if len(self.opponent_all_previous_best_actions) > 0:
            next_best_action = self.opponent_all_previous_best_actions[len(self.opponent_all_previous_best_actions)-1]
            if next_best_action[0] not in self.first_order_projected_perches:
                self.first_order_projected_perches[next_best_action[1]-1] = next_best_action[0]
        # Get the best actions the opponent could have taken (i.e. predict upside down cards based on first order beliefs)
        self.predict_upside_down_cards_first_order()
        
    # Integrate zero order beliefs and first order projections
    def integrate_beliefs(self):
        self.integrated_beliefs = self.current_zero_order_beliefs.copy()
        # Check if the opponent has played any actions that were correctly predicted by this agents zero or first order projections and update confidence accordingly
        self.update_first_order_confidence()
        # Integrate beliefs based on belief integration function: 
        projection = self.previously_projected_first_order_perches[len(self.previously_projected_first_order_perches)-1]
        for perch_index in range(0, len(projection)):
            for belief_index in range(0, len(self.current_zero_order_beliefs)):
                if projection[perch_index] == self.current_zero_order_beliefs[belief_index][0] and perch_index+1 == self.current_zero_order_beliefs[belief_index][1]:
                    # integrated belief = c1 + (1 - c1)*b(0)(s) if s = s_hat(1) 
                    belief_value = self.first_order_confidence_level + (1 - self.first_order_confidence_level)*self.current_zero_order_beliefs[belief_index][2]
                    self.integrated_beliefs[belief_index] = (self.current_zero_order_beliefs[belief_index][0], self.current_zero_order_beliefs[belief_index][1], belief_value)
                elif projection[perch_index] == self.current_zero_order_beliefs[belief_index][0] and perch_index+1 != self.current_zero_order_beliefs[belief_index][1]:
                    # integrated belief = (1 - c1)*b(0)(s) if s != s_hat(1)
                    belief_value = (1 - self.first_order_confidence_level)*self.current_zero_order_beliefs[belief_index][2]
                    self.integrated_beliefs[belief_index] = (self.current_zero_order_beliefs[belief_index][0], self.current_zero_order_beliefs[belief_index][1], belief_value) 

    # Update the confidence of this agents first order beliefs
    def update_first_order_confidence(self):
        correctly_projected = 0
        incorrectly_projected = 0
        # Compare previously projected first order perches with current board state
        for index in range(0, len(self.perches_opponent)):
            for projection in self.previously_projected_first_order_perches:
                correctly_projected = 0
                incorrectly_projected = 0
                if self.perches_opponent[index] != 0 and self.perches_opponent[index] != None and self.perches[index] != 0 and self.perches[index] != None:
                    # If any cards in the current board state have been correctly projected/predicted previously, then increase first-order confidence: c1 = learning_rate + (1 - learning_rate)*c1
                    if projection[index] != None and projection[index] != 0 and projection[index] == self.perches_opponent[index]:
                        correctly_projected += 1
                    # If any cards in the current board state have been incorrectly predicted, then decrease first-order confidence: c1 = (1 - learning_rate)*c1
                    elif projection[index] != None and projection[index] != 0 and projection[index] != self.perches_opponent[index]:
                        incorrectly_projected += 1
            if correctly_projected > 0:
                # c1 = learning_rate + (1 - learning_rate)*c1 
                self.first_order_confidence_level = self.learning_rate + (1 - self.learning_rate)*self.first_order_confidence_level
            if incorrectly_projected > 0:
                # c1 = (1 - learning_rate)*c1
                self.first_order_confidence_level = (1 - self.learning_rate)*self.first_order_confidence_level
        
    # Project opponents perches based on integrated zero and first order beliefs
    def project_perches_first_order_integrated(self):
        # Project perches based on zero order beliefs and keep note of zero order projections to be used to update confidence later
        self.project_perches_zero_order()
        # Project perches based on first order beliefs and keep note of first order projections to be used to update confidence later
        self.project_perches_first_order()
        if self.first_order_projected_perches not in self.previously_projected_first_order_perches:
            self.previously_projected_first_order_perches.append(self.first_order_projected_perches.copy())
        # Get integrated beliefs based zero order beliefs and first order projections
        self.integrate_beliefs()
        # Determine the most probable action the opponent will take based on integrated first order beliefs
        highest_integrated_first_order_belief = self.get_highest_current_belief("First-Order-Integrated")
        self.integrated_first_order_projected_perches = self.perches_opponent.copy()
        # If the opponent still has one action left to play
        if highest_integrated_first_order_belief != None and highest_integrated_first_order_belief != (None, None):
            projected_card = highest_integrated_first_order_belief[0]
            projected_perch = highest_integrated_first_order_belief[1]
            self.integrated_first_order_projected_perches[projected_perch-1] = projected_card 
            # Predict the most likely upside-down cards on the board based on integrated first order beliefs
            predicted_upside_down_cards_integrated_first_order = self.predict_upside_down_cards_integrated_first_order(highest_integrated_first_order_belief)
            for index in range(0, len(predicted_upside_down_cards_integrated_first_order)):
                if predicted_upside_down_cards_integrated_first_order[index] != None and self.integrated_first_order_projected_perches[index] == 0:
                    self.integrated_first_order_projected_perches[index] = predicted_upside_down_cards_integrated_first_order[index]
        
    # Predict upside down cards based on integrated first order beliefs
    def predict_upside_down_cards_integrated_first_order(self, highest_integrated_first_order_belief):
        # For each upside down card currently in the opponents perches, assign most likely value
        most_likely_cards = [None, None, None, None]
        for perch_index in range(0, len(self.perches_opponent)):
            most_likely_card = None
            highest_belief_value = 0
            # If there is an upside down card in the opponents perches, check what the most likely card is to be played there. The
            # predicted upside down cards should not be the same as the the card this agent believes his opponent will play next turn 
            if self.perches_opponent[perch_index] == 0 and highest_integrated_first_order_belief != None: 
                for belief in self.integrated_beliefs:
                    if belief[1] == perch_index+1 and belief[2] >= highest_belief_value and belief[0] != highest_integrated_first_order_belief[0]:
                        most_likely_card = belief[0]
                        highest_belief_value = belief[2]
                most_likely_cards[perch_index] = most_likely_card
        return most_likely_cards

    # Get a list of the most similar board states based on agents zero or first order projections
    def get_most_similar_board_states(self, tom_order, perspective = "Own"):
        # Determine order of ToM
        projection = []
        if tom_order == "Zero-Order" and perspective == "Own":
            self.project_perches_zero_order()
            projection = self.zero_order_projected_perches
        elif tom_order == "Zero-Order" and perspective == "Opponent":
            self.get_opponent_projection_zero_order()
            projection = self.opponent_zero_order_projected_perches
        elif tom_order == "First-Order" and perspective == "Own": 
            self.project_perches_first_order()
            projection = self.first_order_projected_perches 
        elif tom_order == "First-Order-Integrated" and perspective == "Own": 
            self.project_perches_first_order_integrated()
            projection = self.integrated_first_order_projected_perches
        else: 
            print("Error getting most similar board states")
        current_index = 0
        highest_sim_val_agent_board = -1
        highest_sim_val_opponent_board = -1
        sim_agent_pair = 0
        sim_opp_pair = 0
        most_similar_successor_states = []
        # For every payoff pair, determine which state is the most similar to the one 
        # this agent has projected based on the sum of similarity of their own board
        # state and the opponents board state and those in the list of payoff pairs.
        # This gives us a 'highest similarity' value which we can use later to find 
        # the most similar board states to the zero order projected board state.  
        for payoff_pair in self.state_pair_payoffs:
            if tom_order == "Zero-Order" and perspective == "Own":
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection) 
            elif tom_order == "Zero-Order" and perspective == "Opponent":
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches_opponent)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection) 
            elif tom_order == "First-Order" and perspective == "Own":
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection)
            elif tom_order == "First-Order-Integrated" and perspective == "Own":
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection) 
            # Find the greatest similarity values among all states
            if((sim_agent_pair + sim_opp_pair) >= (highest_sim_val_agent_board + highest_sim_val_opponent_board)):
                highest_sim_val_agent_board = sim_agent_pair
                highest_sim_val_opponent_board = sim_opp_pair
            current_index += 1
        current_index = 0
        # Now compile a list of all the most similar board states (using the 'highest similarity' value)
        for payoff_pair in self.state_pair_payoffs:
            if tom_order == "Zero-Order": 
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection)
            elif tom_order == "Zero-Order" and perspective == "Opponent":
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches_opponent)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection)
            elif tom_order == "First-Order-Integrated" and perspective == "Own":
                # Agents Board State
                sim_agent_pair = self.get_levenshtein_similarity(list(payoff_pair[0]), self.perches)
                # Opponents Board State
                sim_opp_pair = self.get_levenshtein_similarity(list(payoff_pair[1]), projection)
            # Add all states with the same highest similarity to a list
            if((sim_agent_pair + sim_opp_pair) >= ((highest_sim_val_agent_board + highest_sim_val_opponent_board))):
                most_similar_successor_states.append(self.state_pair_payoffs[current_index])
            current_index += 1
        return most_similar_successor_states

    # Determine all the winning states the agent can reach. This can be done from this agents 
    # perspective, or from the perspective of his opponent, as to simulate what they would do.
    def get_best_winning_states(self, tom_order, perspective = "Own"):
        # Determine order of ToM
        most_similar_states = []
        if tom_order == "Zero-Order" and perspective == "Own":
            most_similar_states =  self.get_most_similar_board_states("Zero-Order", "Own")
        elif tom_order == "Zero-Order" and perspective == "Opponent":
            most_similar_states =  self.get_most_similar_board_states("Zero-Order", "Opponent")
        elif tom_order == "First-Order" and perspective == "Own": 
            most_similar_states =  self.get_most_similar_board_states("First-Order", "Own")
        elif tom_order == "First-Order-Integrated" and perspective == "Own": 
            most_similar_states =  self.get_most_similar_board_states("First-Order-Integrated", "Own")
        else: 
            print("Error getting best winning states")
        # Get list of most similar states
        state_index = 0
        winning_states = []
        tied_states = []
        highest_value_winning_state = 0
        for payoff_pair in most_similar_states:
            # Determine winner in payoff pair
            winner_of_game = payoff_pair[2][0]
            agent_score = 0
            # Determine overall scores
            agent_score = payoff_pair[2][1]
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

    # Return one of the best actions given the current state (card, perch) representation
    def get_best_action(self, tom_order, perspective = "Own"):
        # Determine order of ToM
        winning_states = []
        player_number = None
        perches = []
        cards = []
        if tom_order == "Zero-Order" and perspective == "Own":
            winning_states = self.get_best_winning_states("Zero-Order", "Own")
            player_number = self.player_number
            perches = self.perches
            cards = self.cards
        elif tom_order == "Zero-Order" and perspective == "Opponent":
            winning_states = self.get_best_winning_states("Zero-Order", "Opponent")
            if self.player_number == 1:
                player_number = 2
            elif self.player_number == 2:
                player_number = 1
            perches = self.perches_opponent
            for index in range(0, len(perches)):
                if perches[index] != None and perches != 0: 
                    cards.append(perches[index])
        elif tom_order == "First-Order" and perspective == "Own":
            winning_states = self.get_best_winning_states("First-Order", "Own")
            player_number = self.player_number
            perches = self.perches
            cards = self.cards
        elif tom_order == "First-Order-Integrated" and perspective == "Own":
            winning_states = self.get_best_winning_states("First-Order-Integrated", "Own")
            player_number = self.player_number
            perches = self.perches
            cards = self.cards
        else: 
            print("Error getting best action")
        
        # Keep track of best (card, perch) pair, along with levenshtein similarity
        best_card_perch_pairs = []
        highest_levenhstein_similarity = 0
        # Play each card on every perch and keep track of the levenhtein similarity
        if winning_states != None:
            for winning_state in winning_states:
                winning_player_state = winning_state[player_number-1]
                for perch_index in range(0, len(perches)):
                    new_state = []
                    # If a valid card can be played on a particular perch, create a new state and compare it with the current winning state
                    if(perches[perch_index] == None):
                        for card in cards:
                            if card != None and card not in perches and card in cards:
                                new_state = perches.copy()
                                new_state[perch_index] = card
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                # Find the highest Levenshtein similarity to a winning state
                                if levenhstein_similarity >= highest_levenhstein_similarity:
                                    highest_levenhstein_similarity = levenhstein_similarity
                        # Get the best (card, perch) pair
                        for card in cards:
                            if card != None and card not in perches and card in cards:
                                new_state = perches.copy()
                                new_state[perch_index] = card
                                # Get Levenshtein Similarity
                                levenhstein_similarity = self.get_levenshtein_similarity(new_state, winning_player_state)
                                # If a high Levenshtein similarity compared to a winning state is found, add the (card, perch) pair to a list of 'good' actions
                                if levenhstein_similarity >= highest_levenhstein_similarity:
                                    best_card_perch_pairs.append((card, perch_index))
                # For each best action the opponent can take, append to list
                for action in best_card_perch_pairs:
                    if action not in self.opponent_all_previous_best_actions:
                        self.opponent_all_previous_best_actions.append(action)
                # Since we have multiple 'good' actions, we choose one of the good actions at random
                if len(best_card_perch_pairs) > 0:
                    return random.choice(best_card_perch_pairs)
                else:
                # If none of the agent actions seem to lead to a winning state, take a random action
                    return (None, None)
        else:
            # If none of the agent actions seem to lead to a winning state, take a random action
            return None

    # Used by this agent to take an action (play a card on a perch and remove card from agents hand)
    def take_action(self, tom_order, perspective = "Own"):
        # Determine order of ToM and perspective, then determine best action
        # 'Perspective' is used to consider actions from the perspective
        # of this agents opponent, or from his own perspective.
        best_action = None
        if tom_order == "Zero-Order" and perspective == "Own":
            best_action = self.get_best_action("Zero-Order", "Own")
        elif tom_order == "Zero-Order" and perspective == "Opponent":
            best_action = self.get_best_action("Zero-Order", "Opponent")
        elif tom_order == "First-Order" and perspective == "Own":
            self.get_best_action("Zero-Order", "Opponent")
            best_action = self.get_best_action("First-Order", "Own")
        elif tom_order == "First-Order-Integrated" and perspective == "Own":
            self.get_best_action("Zero-Order", "Opponent")
            best_action = self.get_best_action("First-Order-Integrated", "Own")
        else: 
            print("Error taking action")
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
        # Clear the projected perches
        self.projected_opponent_perches = [None, None, None, None]

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