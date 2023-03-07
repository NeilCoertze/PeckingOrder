# Class used to define the setup of the zero-order Theory of Mind agent

import random
from . import SimpleAgent

class ZeroOrderAgent(SimpleAgent.SimpleAgent):
    def __init__(self):
        SimpleAgent.SimpleAgent.__init__(self)
        self.beliefs = []               # Beliefs the agent holds regarding the actions of his opponents
                                            # represented as pairs of (card, perch_location, belief_probability)

    # Initialize the state of a newly created agent
    def init_agent(self):
        SimpleAgent.SimpleAgent.init_agent(self)
        self.init_beliefs()

    # Initialize Agents Beliefs about his opponents actions
    def init_beliefs(self):
        for card_num in range(1, 5):
            for perch_num in range(1, 5):
                self.beliefs.append((card_num, perch_num, 0)) # TODO: intialize beliefs to be random upon initialization
        print("Beliefs Are:")
        print(self.beliefs)
    
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

    
                
