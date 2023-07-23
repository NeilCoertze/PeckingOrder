# Class used to define the setup of the game

import Agents.RandomAgent as RA
import Agents.FixedActionAgent as FAA
import Agents.LevenshteinAgent as LA
import Agents.ZeroOrderAgent as ZOA
import Agents.FirstOrderAgent as FOA

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
        print("\n========= GAME INFORMATION =========")
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
        self.select_rounds()

    # Select the number of rounds to play
    def select_rounds(self):
        rounds = ''
        while rounds == '' or type(rounds) != int:
            rounds = int(input("Enter number of games to play: "))

        final_game_displayed = ''
        while final_game_displayed == '' or int(final_game_displayed) not in [1,2]:
            print("\nDisplay Final Game Visually?")
            print("(1) Yes")
            print("(2) No")
            final_game_displayed = int(input())
        win_count = 0
        win_count = self.play_x_games(int(rounds), final_game_displayed)
        print("Player 1 ({}) Wins: {} ({}%)\nPlayer 2 ({}) Wins: {} ({}%)\nDraws: {} ({}%)".format(self.agents[0].get_agent_type(), win_count[0], float(100*(win_count[0])/float(rounds)), self.agents[1].get_agent_type(), win_count[1], 100*(float(win_count[1])/float(rounds)), win_count[2], 100*(float(win_count[2])/float(rounds))))

    # Update the game state (i.e. the state of the perches on the board)
    def update_game_state(self):
        self.agent_one_perches = self.agents[0].get_perches()
        self.agent_two_perches = self.agents[1].get_perches()
        self.update_agent_one_opponent_perch_representation()
        self.update_agent_two_opponent_perch_representation()

        # Update Zero-Order Agent Beliefs

        # If player one is a Zero-Order Agent, update their beliefs
        if self.agents[0].get_agent_type() == "Zero-Order":
            self.agents[0].update_current_zero_order_beliefs()
        # If player two is a Zero-Order Agent, update their beliefs
        if self.agents[1].get_agent_type() == "Zero-Order":
            self.agents[1].update_current_zero_order_beliefs()
        # If player one is a First-Order Agent, update their beliefs

        # Update First-Order Agent Beliefs
        if self.agents[0].get_agent_type() == "First-Order":
            self.agents[0].update_current_zero_order_beliefs()
            self.agents[0].update_current_first_order_beliefs()
        # If player two is a First-Order Agent, update their beliefs
        if self.agents[1].get_agent_type() == "First-Order":
            self.agents[1].update_current_zero_order_beliefs()
            self.agents[1].update_current_first_order_beliefs()

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

    # Display initial menu
    def display_menu(self):
        selection = ''
        while selection == '' or int(selection) not in [1,2,3,4]:
            print("==================== PECKING ORDER ====================")
            print("Please select from menu by entering number:")
            print("(1) Display Game Rules/Information")
            print("(2) Display Agent Descriptions")
            print("(3) Play Game ")
            print("(4) Exit Game ")
            selection = input()
            match int(selection):
                case 1: 
                    self.display_game_information()
                case 2:
                    self.display_agent_descriptions()
                case 3:
                    game_type = ''
                    while game_type == '' or int(game_type) not in [1,2]:
                        print("\nSelect Game Type: ")
                        print("(1) Sequential")
                        print("(2) Simultaneous")
                        game_type = input()
                    match int(game_type):
                        case 1:
                            self.start_game("sequential")
                        case 2: 
                            self.start_game("simultaneous")
                case 4:
                    exit()
                
    # Display Game Rules
    def display_game_information(self):
        print('''
        Pecking Order is a card game in which players compete to control 'perches' on a board by 
        playing bird-themed cards of varying strengths. The version of Pecking Order presented in 
        this model is an altered version of the original game by Richard Garfield. 

        In this version of Pecking Order, each player starts the game with 4 unoccupied perches on 
        their side of the board and 4 cards. Cards are numbered 1-4, with higher value cards being 
        'stronger'. During each round, both players must play one of their cards face-down on an 
        unoccupied perch on their side of the board. If both players have played a face-down card 
        on the same perch location on opposite sides of the board, the cards are flipped over, and 
        the player who played the higher value card on that perch gains control of said perch.   
        
        The number of points earned by gaining control of a particular perch is equal to the index of 
        the perch (i.e. perch 1 = 1 point, perch 2 = 2 points, perch 3 = 3 points, perch 4 = 4 points).
        Note that the player who is not in control of a perch gains no points.

        When both players have played all their cards and all perches are occupied, all cards will be 
        face-up, at which points each player can determine their final score by taking the sum of the 
        points gained by controlling a particular perch. 

        This project aims to evaluate how game structure affects the effectiveness of higher-order theory
        of mind. As such, there are two possible ways for the game to be played (these can be selected when
        running the model). Firstly, the game can be played 'sequentially', meaning players take turns playing
        their cards in a "I play, you play, I play, repeat" fashion. Alternatively, the game can be played
        'simultaneously', meaning players play their cards at the same time during each round.

        In this project, we model a few different types of players (referred to as agents), each with differing
        strategies or differing levels of theory of mind. More information about these agents can be found in 
        the "Display Agent Descriptions" section of the main menu.
        ''')
        selection = input("Enter (1) to return to the main menu\n")
        while selection == '' or int(selection) != 1:
            selection = input("Enter (1) to return to the main menu\n")
        self.display_menu()

    # Display agent descriptions
    def display_agent_descriptions(self):
        selection = ''
        while selection == '' or int(selection) not in [1,2,3,4,5]:
            print("\nSelect Agent Type for Description: \n")
            print("(1) Random Action Agent")
            print("(2) Fixed Action Agent")
            print("(3) Levenshtein Agent")
            print("(4) Zero-Order Agent")
            print("(5) First-Order Agent")
            print("(6) Main Menu\n")
            selection = input()
            if selection != '':
                match int(selection):
                    case 1:
                        print('''
                The Random Action Agent chooses a random card to play on a random perch
                each turn.
                        ''')
                    case 2: 
                        print(''' 
                The Fixed Action agent plays fixed actions each turn, by default the fixed
                actions played are [1,2,3,4], where each value of card is played on the perch
                with the same value.
                        ''')
                    case 3: 
                        print(''' 
                The Levenshtein Agent generates all possible end-game states, where both players
                have played all their cards. Following this, it evaluates the outcome of those 
                end-game states, including the winner of the game along with each players final 
                score. 
                    
                During each turn, the Levenshtein Agent compares the current board state (his own 
                as well as his opponents perches along with the cards that occupy them), with each 
                of the final end-game states. Using the Levenshtein similarity metric, this agent 
                determines the most similar end-game states to the current board state. Next, this 
                agent filters out all end-game states that do not result in a win for him. If there
                are no winning end-game states similar to the current state, this agent instead 
                considers states in which it ties, as this is ultimately more favorable than a loss.  

                The Levenshtein Agent then looks at the list of compiled end-game states most similar
                to the current board state, and simulates playing each of his cards on each remaining
                unoccupied perch in his current board state. For each newly generated state, this is 
                compared with the current end-game state the agent is looking at using the Levenshtein 
                similarity metric mentioned before. This allows the agent to determine which action
                will result in the board state most closely resembling a winning state for this agent.

                If there are multiple actions that each yield the same similarity value, this agent
                randomly selects one of those actions at random. If there is only one 'good' action,
                the agent selects that action. Finally, if no actions appear to lead to a winning or
                tied state, the agent plays a random action in the same manner as the Random Action 
                Agent. 
                        ''')
                    case 4: 
                        print(''' 
                The Zero-Order Agent evaluates the current board state and his next best actions in a 
                similar manner to the Levenshtein Agent. However, this agent also holds Zero-Order 
                beliefs about the actions of his opponent. These beliefs are represented as a list of
                tuples, with each entry corresponding to a belief value of a particular card being 
                played on a particular perch in the form: (card, perch, belief value). For example,
                the tuple (1, 2, 0.23) represents a 23% belief that card 1 will be played on perch 2
                by this agents opponent. These beliefs are referred to as Zero-Order beliefs.

                Furthermore, this agent maintains two belief systems, one for its overall beliefs, and
                one for its current beliefs. The overall beliefs persist throughout the duration of all
                games played, only being updated at the end of each game when all cards have been revealed.
                These beliefs give the agent an indication of the overall tendencies of his opponent, not
                taking into consideration the current board state, but instead the trends throughout all
                previously played games. Note that this agents overall beliefs are initialized randomly
                upon the instatiation of the agent.
                
                Throughout the course of the game, this agents current beliefs are updated to better suit the 
                current game state. As an example, if the opponent plays card 1 on perch 2, this means that 
                no other cards can be played on perch 2, and similarly that card 1 can not be played elsewhere. 
                As such, all current beliefs about other cards being played on perch 2 are set to zero, and 
                all current beliefs about card 1 being played on other perches are also set to zero. 

                At the start of each game, this agents current beliefs are set to its overall beliefs, then 
                progressively updated after each round in the game. 

                When updating his overall beliefs, this agent makes use of a learning rate, which is specified
                by the user upon running the model. The learning rate affects how quickly this agent updates
                its beliefs. In other words, the higher the learning rate, the greater the increase in a particular
                belief after encountering a certain card on a certain perch. 

                Using its Zero-Order beliefs, this agent predicts what the values of its opponents upside down cards
                may be, as well as the next most likely card the opponent will on their next turn. For example, if the
                opponent has an upside down card on perch 2, and this agent has a high belief that the opponent is 
                likely to play card 1 on perch 2, then it will predict that the opponents board state contains card 1 
                on perch 2. Moreover, if the opponent has no cards on perch 4, and this agent has a high belief value
                that card 3 will be played on perch 4, the it will project the opponents future board state to contain 
                card 3 on perch 4. 

                Using predictions and projections, this agent can use the same Levenshtein similarity metric to determine
                similar winning board states and winning actions as the Levenshtein Agent, but with more predicted certainty.
                When the Levenshtein agent compares his opponents board state to a final board state each round, any upside 
                down cards remain upside down, meaning the similarity comparisons are more limited in information, thus 
                (possibly) less reliable. By predicting and projecting the opponents board state, the Zero-Order Agent is able
                to make more accurate measures of similarity, and thus determine the best possible move to make with more 
                certainty (at least according to his beliefs). 
                        ''')
                    case 5: 
                        print(''' 
                The First-Order Agent maintains the same Zero-Order beliefs as the Zero-Order Agent, however it also
                maintains beliefs about what its opponent may believe. These beliefs are referred to as First-Order 
                beliefs. In order to form beliefs about what his opponents believes, this agent simulates what it would
                believe in the position of his opponent. As such, this agent views the board from the perspective of his 
                opponent, meaning any upside down cards from the perspective of his opponent are considered as such, and
                all predictions and projections are made based on the current board state, overall and current First-Order
                beliefs. 

                Note that this agent does not actually know whether or not his opponent has any beliefs, or if they are 
                simply playing according to some preset strategy (e.g. the Fixed-Action Agent). As such, this agent 
                also maintains a First-Order confidence level, which determines how much his First-Order beliefs influences
                his decisions throughout the game. When deciding on his next action, this agent integrates his Zero-Order and 
                First-Order beliefs using the First-Order confidence level. A higher first order confidence level means the
                agent is more likely to play according to his First-Order beliefs, whereas a lower confidence level means the 
                agent is more likely to play according to his Zero-Order beliefs. 

                This agent also makes use of a learning rate to determine how quickly its beliefs should be updated upon 
                encountering a certain card on a certain perch. 
                        ''')
                    case 6: 
                        self.display_menu()

    # Select Agents from user to use in game
    def start_game(self, game_type):
        agent_one = None
        agent_two = None
        agent_one_type = ''
        agent_two_type = ''

        while agent_one_type == '' or int(agent_one_type) not in [1,2,3,4,5]: 
            print("\nSelect Agent 1 Type: ")
            print("(1) Random Action Agent")
            print("(2) Fixed Action Agent")
            print("(3) Levenshtein Agent")
            print("(4) Zero-Order Agent")
            print("(5) First-Order Agent")
            agent_one_type = input()
            match int(agent_one_type):
                case 1:
                    agent_one = RA.RandomAgent()
                    agent_one.init_agent(1)
                case 2:
                    agent_one = FAA.FixedActionAgent()
                    agent_one.init_agent(1)
                case 3: 
                    agent_one = LA.LevenshteinAgent()
                    agent_one.init_agent(1)
                case 4: 
                    agent_one = ZOA.ZeroOrderAgent()
                    learning_rate = ''
                    while learning_rate == '' or learning_rate < 0 or learning_rate > 1:
                        learning_rate = float(input("Enter Learning Rate (between 0 and 1): "))
                    agent_one.init_agent(1, learning_rate)
                case 5:
                    agent_one = FOA.FirstOrderAgent()
                    learning_rate = ''
                    while learning_rate == '' or int(learning_rate) < 0 or int(learning_rate) > 1:
                        learning_rate = float(input("Enter Learning Rate (between 0 and 1): "))
                    confidence_level = ''
                    while confidence_level == '' or int(confidence_level) < 0 or int(confidence_level) > 1:
                        confidence_level = float(input("Enter First-Order Confidence Level (between 0 and 1): "))
                    agent_one.init_agent(1, learning_rate, confidence_level)

        while agent_two_type == '' or int(agent_two_type) not in [1,2,3,4,5]: 
                print("\nSelect Agent 2 Type: ")
                print("(1) Random Action Agent")
                print("(2) Fixed Action Agent")
                print("(3) Levenshtein Agent")
                print("(4) Zero-Order Agent")
                print("(5) First-Order Agent")
                agent_two_type = int(input())
                match int(agent_two_type):
                    case 1:
                        agent_two = RA.RandomAgent()
                        agent_two.init_agent(2)
                    case 2:
                        agent_two = FAA.FixedActionAgent()
                        agent_two.init_agent(2)
                    case 3: 
                        agent_two = LA.LevenshteinAgent()
                        agent_two.init_agent(2)
                    case 4: 
                        agent_two = ZOA.ZeroOrderAgent()
                        learning_rate = float(input("Enter Learning Rate: "))
                        agent_two.init_agent(2, learning_rate)
                    case 5:
                        agent_two = FOA.FirstOrderAgent()
                        learning_rate = ''
                        while learning_rate == '' or int(learning_rate) < 0 or int(learning_rate) > 1:
                            learning_rate = float(input("Enter Learning Rate (between 0 and 1): "))
                        confidence_level = ''
                        while confidence_level == '' or int(confidence_level) < 0 or int(confidence_level) > 1:
                            confidence_level = float(input("Enter First-Order Confidence Level (between 0 and 1): "))
                        agent_two.init_agent(2, learning_rate, confidence_level)
        self.init_game(agent_one, agent_two, game_type)

    # Play a single round of Pecking Order
    def play_one_round(self):
        if(self.game_type == "sequential"):
            if self.agents[0].get_agent_type() == "First-Order":
                self.agents[0].take_action("First-Order")
            else:
                self.agents[0].take_action()
            self.update_game_state()
            if self.agents[1].get_agent_type() == "First-Order":
                self.agents[1].take_action("First-Order")
            else:
                self.agents[1].take_action()
            self.update_game_state()
        elif(self.game_type == "simultaneous"):
            if self.agents[0].get_agent_type() == "First-Order":
                self.agents[0].take_action("First-Order")
            else:
                self.agents[0].take_action()
            if self.agents[1].get_agent_type() == "First-Order":
                self.agents[1].take_action("First-Order")
            else:
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
    def play_x_games(self, rounds=50, final_game_displayed = 2):
        total_wins_player_one = 0
        total_wins_player_two = 0
        total_draws = 0
        # Play a x number of games
        for i in range(0, rounds):
            print("Playing Game: ", i+1)
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
        # Play final game displayed
        if final_game_displayed == 1:
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

