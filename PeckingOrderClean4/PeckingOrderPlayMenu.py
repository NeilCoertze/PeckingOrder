# This class is used to instantiate and play games of Pecking Order

import Agents.RandomAgent as RA
import Agents.FixedActionAgent as FAA
import Agents.LevenshteinAgent as LA
import Agents.ZeroOrderAgent as ZOA
import Agents.FirstOrderAgent as FOA
import PeckingOrderGame as POG

# # Instantiate the Pecking Order Game
PeckingOrderGame = POG.PeckingOrderGame()
PeckingOrderGame.display_menu()
