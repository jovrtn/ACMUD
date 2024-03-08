
from .objects import Object
from evennia.typeclasses.attributes import AttributeProperty
from enums import WeeniePropBool


class Lifestone(Object):
    """
    Class for lifestones
    """

    name_color = "|035"

  
    def at_pre_use(self, user, **kwargs):

        # hello

        return True

    def use(self, user, **kwargs):

        # What happens when a player uses this?

        # Deduct stamina from target

        user.home = self.location

        user.msg(
            "|035You have attuned your spirit to this Lifestone. You will resurrect here after you die.|n ")
        new_stamina = round(user.vitals.stamina.current / 2)
        #user.vitals.stamina.current = new_stamina
        user.vitals.update_vital('stamina', new_stamina)

    def at_post_use(self, user, **kwargs):

        # What happens when a player uses this?
        # dfdf

        pass
