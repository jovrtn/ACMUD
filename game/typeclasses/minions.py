
from .creatures import Creature


class Minion(Creature):
    """
    This is a base class for minions.
    """

    def move_around(self):
        print(f"{self.key} is moving!")