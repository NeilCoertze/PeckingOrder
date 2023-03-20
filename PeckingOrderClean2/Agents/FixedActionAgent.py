""" 
Class used to define the setup of the Fixed Action Agent. This agent performs the same actions repeatedly. 
"""
import sys, os
sys.path.append(os.getcwd())

import random
from Agents import RandomAgent

class FixedActionAgent(RandomAgent.RandomAgent):
    def __init__(self):
        RandomAgent.RandomAgent.__init__(self)
        self.cards_to_play = []
        
    # Initialize the state of a newly created agent
    def init_agent(self, player_number):
        RandomAgent.RandomAgent.init_agent(self, player_number)
        self.cards_to_play = [1,2,3,4]
        self.agent_type = "Fixed-Action"

    # Reset the agent
    def reset_agent(self):
        self.cards = [1, 2, 3, 4]
        self.cards_to_play = [1,2,3,4]
        self.perches = [None, None, None, None]
        self.perches_opponent = [None, None, None, None]

    # Used for an agent to take an action (play a card on a perch and remove card from agents hand)
    def take_action(self):
        # Play the same sequence of cards every round
        for i in range(0, len(self.perches)):
            if self.perches[i] == None:
                if len(self.cards_to_play) > 0:
                    card_to_play = self.cards_to_play[0]
                    self.perches[i] = card_to_play
                    self.cards[card_to_play-1] = None
                    self.cards_to_play.pop(0)
                    break
                

    
                
