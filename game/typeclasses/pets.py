
from .creatures import Creature


class Pet(Creature):
    """
    This is a base class for pets.
    """

    def move_around(self):
        print(f"{self.key} is moving!")