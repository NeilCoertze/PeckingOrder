# Class used to define the setup of the board

class PeckingOrderGame:
    def __init__(self):
        self.agents = []
        self.agent_one_perches = []    # Perches located on agent ones side of the board 
        self.agent_two_perches = []    # Perches located on agent twos side of the board 
        # self.all_states = []           # A set of all possible states in the game
        # self.action_pairs = []         # A set of all possible action pairs
        # self.all_payoffs = []          # A set of all possible payoffs based on the game states (use tuples page 40)

    # Add agents to the game
    def add_agents(self, agent_one, agent_two):
        self.agents.append(agent_one)
        self.agents.append(agent_two)
    
    # Initialize the perches for both agents playing the game
    def init_agent_perches(self):
        self.agent_one_perches = [None, None, None, None]
        self.agent_two_perches = [None, None, None, None]
    
    # # Initialize all possible states in the game
    # def init_all_states(self):
    #     pass

    # # Initialize all possible action pairs
    # def init_all_action_pairs(self):
    #     pass

    # # Initialize the payoff matrix for all possible states of the game
    # def init_all_payoffs(self):
    #     pass

    # Initialize the Pecking Order game
    def init_game(self, agent_one, agent_two):
        self.add_agents(agent_one, agent_two)
        self.init_agent_perches()
        # self.init_all_states()
        # self.init_all_action_pairs()
        # self.init_all_payoffs()

    # Update the game state (i.e. the state of the perches on the board)
    def update_game_state(self):
        self.agent_one_perches = self.agents[0].get_perches()
        self.agent_two_perches = self.agents[1].get_perches()
        self.update_agent_one_opponent_perch_representation()
        self.update_agent_two_opponent_perch_representation()

    # Update agent ones represenation of their opponents perches
    def update_agent_one_opponent_perch_representation(self):
        perches_opponent = []
        for i in range(0,4):
            # If both not None, agent can see opponents card value
            if self.agent_one_perches[i] != None and self.agent_two_perches[i] != None:
                perches_opponent.append(self.agent_two_perches[i])
            # If agent one has not played a card on a perch but agent two has
            elif self.agent_one_perches[i] == None and self.agent_two_perches[i] != None:
                perches_opponent.append(0)
            # if opponent has not played a card on a perch
            elif self.agent_two_perches[i] == None:
                perches_opponent.append(None)
        self.agents[0].set_perches_opponent(perches_opponent)
    
    # Update agent twos represenation of their opponents perches
    def update_agent_two_opponent_perch_representation(self):
        perches_opponent = []
        for i in range(0,4):
            # If both not None, agent can see opponents card value
            if self.agent_one_perches[i] != None and self.agent_two_perches[i] != None:
                perches_opponent.append(self.agent_one_perches[i])
            # If agent two has not played a card on a perch but agent one has
            elif self.agent_two_perches[i] == None and self.agent_one_perches[i] != None:
                perches_opponent.append(0)
            # if opponent has not played a card on a perch
            elif self.agent_one_perches[i] == None:
                perches_opponent.append(None)
        self.agents[1].set_perches_opponent(perches_opponent)

    # Play a single round of Pecking Order
    def play_one_round(self, sequential_or_simultaneous):
        if(sequential_or_simultaneous == "sequential"):
            self.agents[0].take_action()
            self.update_game_state()
            self.agents[1].take_action()
            self.update_game_state()
            
        elif(sequential_or_simultaneous == "simultaneous"):
            self.agents[0].take_action()
            self.agents[1].take_action()
            self.update_game_state()
            
    # Play a full game of Pecking Order
    def play_full_game(self, sequential_or_simultaneous):
        while((None in self.agent_one_perches) or (None in self.agent_two_perches)):
            self.play_one_round(sequential_or_simultaneous)
        self.show_final_game_state()

    # Play a full game of Pecking Order
    def play_full_game_displayed(self, sequential_or_simultaneous):
        while((None in self.agent_one_perches) or (None in self.agent_two_perches)):
            self.play_one_round(sequential_or_simultaneous)
            self.show_board_state()
        self.show_final_game_state()

    # Play multiple games, return count of wins/losses per player
    def play_x_games(self, sequential_or_simultaneous, x):
        total_wins_player_one = 0
        total_wins_player_two = 0
        total_draws = 0
        # Play a x number of games
        for i in range(0, x):
            #= print("Game: ", str(i))
            # Play single game and keep track of wins
            while((None in self.agent_one_perches) or (None in self.agent_two_perches)):
                self.play_one_round(sequential_or_simultaneous)
            #= print("########## FINAL (Current) BOARD STATE #################")
            #= self.show_board_state()
            winner = self.determine_winner()
            #= print("Winner is: {}".format(winner))
            #.. print("#############################################\n\n")
            if winner[0] == 1:
                total_wins_player_one += 1
            elif winner[0] == 2:
                total_wins_player_two += 1
            elif winner[0] == 0:
                total_draws += 1
            # Reset game state in order to play new game (i.e. reset player perches)
            self.reset_game()
        return (total_wins_player_one, total_wins_player_two, total_draws)

    # Reset the board state and the agents
    def reset_game(self):
        self.init_agent_perches()
        self.agents[0].reset_agent()
        self.agents[1].reset_agent()

    # Display current board state
    def show_board_state(self):
        print("\n================ CURRENT =================")
        print("        Current Board State        ")
        print("-----------------------------------")
        print("Agent One Cards: " + str(self.agent_one_perches))
        print("Agent Two Cards: " + str(self.agent_two_perches))
        print("-----------------------------------")
        self.show_agent_one_opponent_perch_representation()
        self.show_agent_two_opponent_perch_representation()
        print("==========================================\n")

    # Display representation of agent ones opponents perches
    def show_agent_one_opponent_perch_representation(self):
        print("Agent One Opponent Perch Representation:")
        print(self.agents[0].get_perches_opponent())

    # Display representation of agent twos opponents perches
    def show_agent_two_opponent_perch_representation(self):
        print("Agent Two Opponent Perch Representation:")
        print(self.agents[1].get_perches_opponent())

    # Display the final game state
    def show_final_game_state(self):
        winner, agent_one_score, agent_two_score = self.determine_winner()

        print("================ FINAL ===================")
        if(winner == 1):
            print("Winner is Agent One!" )
            print("Agent One Score: " + str(agent_one_score))
            print("Agent Two Score: " + str(agent_two_score))
        elif(winner == 2):
            print("Winner is Agent Two!" )
            print("Agent One Score: " + str(agent_one_score))
            print("Agent Two Score: " + str(agent_two_score))
        print("-----------------------------------")
        print("Final Game State is:")
        print("Agent One Cards: " + str(self.agent_one_perches))
        print("Agent Two Cards: " + str(self.agent_two_perches))
        print("===========================================")


    # Return the winner of the game along with their score (return: 1 for agent one, 2 for agent two)
    def determine_winner(self):
        agent_one_score = 0
        agent_two_score = 0

        # Highest Value Perch (4 points)
        if self.agent_one_perches[3] > self.agent_two_perches[3]:
            agent_one_score += 4
        elif self.agent_one_perches[3] < self.agent_two_perches[3]:
            agent_two_score += 4
        
        # Second-Highest Value Perch (3 points)
        if self.agent_one_perches[2] > self.agent_two_perches[2]:
            agent_one_score += 3
        elif self.agent_one_perches[2] < self.agent_two_perches[2]:
            agent_two_score += 3

        # Second-Lowest Value Perch (2 points)
        if self.agent_one_perches[1] > self.agent_two_perches[1]:
            agent_one_score += 2
        elif self.agent_one_perches[1] < self.agent_two_perches[1]:
            agent_two_score += 2
        
        # Lowest Value Perch (1 points)
        if self.agent_one_perches[0] > self.agent_two_perches[0]:
            agent_one_score += 1
        elif self.agent_one_perches[0] < self.agent_two_perches[0]:
            agent_two_score += 1

        # Tie-Breaker
        if agent_one_score > agent_two_score:
            # Agent one wins
            return (1, agent_one_score, agent_two_score)
        elif agent_one_score < agent_two_score:
            # Agent two wins
            return (2, agent_one_score, agent_two_score)
        else:
            if self.agent_one_perches[0] > self.agent_two_perches[0]:
                # Agent one wins
                return (1, agent_one_score, agent_two_score)
            elif self.agent_one_perches[0] < self.agent_two_perches[0]:
                # Agent two wins
                return (2, agent_one_score, agent_two_score)
            else:
                return (0, agent_one_score, agent_two_score)

