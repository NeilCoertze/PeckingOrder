# Class used to define the setup of the agents

import random

class SimpleAgent:
    def __init__(self):
        self.cards = []                 # The cards this agent has available to play
        # self.cards_opponent = []      # The cards the opponent likely still has in their hand
        self.perches = []               # The cards the agent has placed on their perches currently
        self.perches_opponent = []      # The cards the opponent has placed on their perches currently (0 = unknown)
        self.player_number = 0

    # Initialize the state of a newly created agent
    def init_agent(self, player_number):
        self.cards = [1, 2, 3, 4]
        # self.cards_opponent = [0, 0, 0, 0]
        self.perches = [None, None, None, None]
        self.perches_opponent = [None, None, None, None]
        self.player_number = player_number

    # Reset the agent
    def reset_agent(self):
        self.cards = [1, 2, 3, 4]
        # self.cards_opponent = [0, 0, 0, 0]
        self.perches = [None, None, None, None]
        self.perches_opponent = [None, None, None, None]

    # Set the opponents cards that this player can see in their perch location
    def set_perches_opponent(self, perches_opponent):
        self.perches_opponent = perches_opponent
    
    # Return the perches this agent has occupied
    def get_perches(self):
        return self.perches
    
    # Returns the cards the opponent has placed on their perches currently (0 = unknown, None = None)
    def get_perches_opponent(self):
        return self.perches_opponent

    # Returns the current state of the agent and the opponents perches
    def get_perch_state(self):
        return (self.get_perches(), self.get_perches_opponent())

    # Used for an agent to take an action (play a card on a perch and remove card from agents hand)
    # TODO: for now, actions are taken randomly to test funtionality of game -> inheritance + overload function for ToM_0 and ToM_1 agents
    def take_action(self):
        actionValid = False
        while(not actionValid):
            card_to_play = random.randint(1,4)
            perch_to_play = random.randint(1,4)
            if((self.cards[card_to_play-1] != None) and (self.perches[perch_to_play-1] == None)):
                actionValid = True
                self.perches[perch_to_play-1] = card_to_play
                self.cards[card_to_play-1] = None
                
