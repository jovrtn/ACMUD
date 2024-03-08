from .objects import Object
from evennia.typeclasses.attributes import AttributeProperty

class Container(Object):
    """
    This is a generic container
    """

    @property
    def slots_open(self):
        return self.size - len(self.contents)

    @property
    def add(self, obj):
        obj.move_to(self)


