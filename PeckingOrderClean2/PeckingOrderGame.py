# Class used to define the setup of the board

class PeckingOrderGame:
    def __init__(self):
        self.agents = []
        self.agent_one_perches = []    # Perches located on agent ones side of the board 
        self.agent_two_perches = []    # Perches located on agent twos side of the board 
        self.game_type = None          # The type of game (sequential or simultaneous)
        
    # Add agents to the game
    def add_agents(self, agent_one, agent_two):
        self.agents.append(agent_one)
        self.agents.append(agent_two)
    
    # Display game initialization information
    def show_game_initialization(self):
        print("========= GAME INFORMATION =========")
        print("Game Type: ", self.game_type)
        print("AgentOne: {} | AgentTwo: {}".format(self.agents[0].get_agent_type(), self.agents[1].get_agent_type()))
        print("====================================")

    # Initialize the perches for both agents playing the game
    def init_agent_perches(self):
        self.agent_one_perches = [None, None, None, None]
        self.agent_two_perches = [None, None, None, None]

    # Initialize the Pecking Order game
    def init_game(self, agent_one, agent_two, game_type):
        self.add_agents(agent_one, agent_two)
        self.init_agent_perches()
        self.game_type = game_type
        self.show_game_initialization()

    # Update the game state (i.e. the state of the perches on the board)
    def update_game_state(self):
        self.agent_one_perches = self.agents[0].get_perches()
        self.agent_two_perches = self.agents[1].get_perches()
        self.update_agent_one_opponent_perch_representation()
        self.update_agent_two_opponent_perch_representation()
        # If player one is a Zero-Order Agent, update their beliefs
        if self.agents[0].get_agent_type() == "Zero-Order":
            self.agents[0].update_current_beliefs()
        # If player two is a Zero-Order Agent, update their beliefs
        if self.agents[1].get_agent_type() == "Zero-Order":
            self.agents[1].update_current_beliefs()

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
    def play_one_round(self):
        if(self.game_type == "sequential"):
            self.agents[0].take_action()
            self.update_game_state()
            self.agents[1].take_action()
            self.update_game_state()
            
        elif(self.game_type == "simultaneous"):
            self.agents[0].take_action()
            self.agents[1].take_action()
            self.update_game_state()
            
    # Play a full game of Pecking Order
    def play_full_game(self):
        while((None in self.agent_one_perches) or (None in self.agent_two_perches)):
            self.play_one_round()
        self.show_final_game_state()

    # Play a full game of Pecking Order
    def play_full_game_displayed(self):
        while((None in self.agent_one_perches) or (None in self.agent_two_perches)):
            self.play_one_round()
            self.show_board_state()
        self.show_final_game_state()

    # Play multiple games, return count of wins/losses per player
    def play_x_games(self, x=50):
        total_wins_player_one = 0
        total_wins_player_two = 0
        total_draws = 0
        # Play a x number of games
        for i in range(0, x):
            # Play single game and keep track of wins
            while((None in self.agent_one_perches) or (None in self.agent_two_perches)):
                self.play_one_round()
            winner = self.determine_winner()
            if winner[0] == 1:
                total_wins_player_one += 1
            elif winner[0] == 2:
                total_wins_player_two += 1
            elif winner[0] == 0:
                total_draws += 1
            # Reset game state in order to play new game (i.e. reset player perches)
            self.reset_game()
        # DEBUG play final game
        self.play_full_game_displayed()
        return (total_wins_player_one, total_wins_player_two, total_draws)

    # Reset the board state and the agents
    def reset_game(self):
        self.agents[0].reset_agent()
        self.agents[1].reset_agent()
        self.init_agent_perches()

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

