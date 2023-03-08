# taken from The Hitchhiker's Guide To Python

import os
import sys

# add module path to search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import used modules
from historian import Historian, HistorianMixin
