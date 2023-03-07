# Class used to define the setup of the zero-order Theory of Mind agent

import random
import OptimalAgent

class ZeroOrderAgent(OptimalAgent.OptimalAgent):
    def __init__(self):
        OptimalAgent.OptimalAgent.__init__(self)
        self.beliefs = []               # Beliefs the agent holds regarding the actions of his opponents
                                            # represented as pairs of (card, perch_location, belief_probability)

    # Initialize the state of a newly created agent
    def init_agent(self, player_number):
        OptimalAgent.OptimalAgent.init_agent(self, player_number)
        self.init_beliefs()

    # Initialize Agents Beliefs about his opponents actions
    def init_beliefs(self):
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
                self.beliefs.append((card_num, perch_num, proportional_arr[iterator]))
                iterator += 1
        # print("Beliefs Are:")
        # print(self.beliefs)
        belief_total = 0
        for i in range(0, len(self.beliefs)):
            belief_total += self.beliefs[i][2]
        # print("Sum of Beliefs Init: ", belief_total)

    # Update belief probabilties by a particular value
    # TODO: Include learning rate here instead of a fixed probability increase of 5%.
    #       A higher learning rate should cause the probability to increase more 
    #       drastically, whereas a lower learning rate should cause the probability 
    #       to increase at a slower rate
    def increase_belief_probability(self, card, perch): 
        # Calculate the sum of the belief probabilities
        total = 0
        iterator = 0
        belief_index = None
        beliefs_as_list = []
        for belief in self.beliefs:
            total += belief[2]
            beliefs_as_list.append(belief[2])
            # Find the index of the belief to be adjusted
            if belief[0] == card and belief[1] == perch:
                belief_index = iterator
            iterator += 1
        
        # If an index is specified, increase the corresponding random number by 5%
        if belief_index is not None:
            beliefs_as_list[belief_index] += 0.05
            total += 0.05
        
        # Calculate the probabilities by dividing each random number by the total
        new_belief_probabilities = [x / total for x in beliefs_as_list]

        # Assign new belief probabilities to self.beliefs        
        for i in range(0, len(self.beliefs)):
            self.beliefs[i] = (self.beliefs[i][0], self.beliefs[i][0], new_belief_probabilities[i])
        
        belief_total = 0
        for i in range(0, len(self.beliefs)):
            belief_total += self.beliefs[i][2]
            #print("i is: ", i)
        # print("Sum of Beliefs Increased: ", belief_total)

    # Get beliefs of agent
    def get_beliefs(self):
        return self.beliefs
    
    # Update Belief Value for specific card on specific perch
    def update_single_belief(self, card_num, perch_num, belief_value):
        for index in range(0, len(self.beliefs)):
            if (self.beliefs[index][0] == card_num) and (self.beliefs[index][1] == perch_num):
                new_belief = list(self.beliefs[index])
                new_belief[2] = belief_value
                self.beliefs[index] = tuple(new_belief)

    # Used for an agent to take an action (play a card on a perch and remove card from agents hand)
    # TODO: for now, actions are taken randomly, but they should be based on a value function and 
    #       decision function. There will also be a belief updating function that will allow agents
    #       to update their beliefs about what their opponent will do. 
    def take_action(self):
        actionValid = False
        while(not actionValid):
            card_to_play = random.randint(1,4)
            perch_to_play = random.randint(1,4)
            if((self.cards[card_to_play-1] != None) and (self.perches[perch_to_play-1] == None)):
                actionValid = True
                self.perches[perch_to_play-1] = card_to_play
                self.cards[card_to_play-1] = None

    
                
