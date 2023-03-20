# A definition of a board state in Pecking Order

class BoardState:
    def __init__(self):
        self.agent_one_perches = []
        self.agent_two_perches = []
        self.neighboring_states = []
        self.neighboring_states_value_estimates = []
