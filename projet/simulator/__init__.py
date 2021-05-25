# this relative import exposes the classes themselves in the namespace 'simulator'
# that is why in main.py you can write 'from simulator import World'
# instead of 'from simulator.datastructures.world import World'
from .utils.world import World, Body

from .simulator import Simulator
