# Class used to define the setup of the agents

import random

class RandomAgent:
    def __init__(self):
        self.cards = []                 # The cards this agent has available to play
        self.perches = []               # The cards the agent has placed on their perches currently
        self.perches_opponent = []      # The cards the opponent has placed on their perches currently (0 = unknown)
        self.player_number = None       # The player number, used to keep track of which player is which internally
        self.agent_type = None          # The type of agent that is playing

    # Initialize the state of a newly created agent
    def init_agent(self, player_number):
        self.cards = [1, 2, 3, 4]
        self.perches = [None, None, None, None]
        self.perches_opponent = [None, None, None, None]
        self.player_number = player_number
        self.agent_type = "Simple"

    # Reset the agent
    def reset_agent(self):
        self.cards = [1, 2, 3, 4]
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

    # Used by an agent to take a random action (play a card on a perch and remove that card from agents hand)
    def take_action(self):
        actionValid = False
        while(not actionValid):
            card_to_play = random.randint(1,4)
            perch_to_play = random.randint(1,4)
            if((self.cards[card_to_play-1] != None) and (self.perches[perch_to_play-1] == None)):
                actionValid = True
                self.perches[perch_to_play-1] = card_to_play
                self.cards[card_to_play-1] = None
                
    def get_agent_type(self):
        return self.agent_type
