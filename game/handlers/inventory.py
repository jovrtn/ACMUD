"""
Knave has a system of Slots for its inventory.

"""

from evennia.utils.utils import inherits_from
from typeclasses.containers import Container
from evennia.utils.create import create_object

# from ..enums import Ability, WieldLocation
# from .objects import EvAdventureObject, get_bare_hands


NUM_CONTAINER_SLOTS_BASE = 7


class InventoryError(TypeError):
    pass


class InventoryHandler:
    """
    Custom inventory handler

    """

    save_attribute = "_inventory"

    def __init__(self, obj):
        # here obj is the character we store the handler on
        self.obj = obj
        self._load()

    def _load(self):
        """Load our data from an Attribute on `self.obj`"""

        containers = {
            "equipped": {},
            "backpack": None,
            "packs": []
        }

        # num_pack_slots = NUM_CONTAINER_SLOTS_BASE

        # for num_pack in range(num_pack_slots):
        #     packs["pack_" + str(num_pack)] = None

        containers = self.obj.attributes.get(
            self.save_attribute,
            category="inventory",
            default=containers
        )

        for container, value in containers.items():
            setattr(self, container, value)

    def _save(self):
        """Save our data back to the same Attribute"""

        containers = {
            "equipped": self.equipped,
            "backpack": self.backpack,
            "packs": self.packs
        }

        self.obj.attributes.add(self.save_attribute,
                                containers, category="inventory")
