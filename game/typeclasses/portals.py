from .objects import Object
from evennia.typeclasses.attributes import AttributeProperty
from enums import WeeniePropPosition


class Portal(Object):
    """
    This is a base class for portal.
    """

    name_color = "|515"

    def at_pre_use(self, user, **kwargs):

        # hello

        return True

    def use(self, user, **kwargs):

        # What happens when a player uses this?

        # Deduct stamina from target

        user.msg(
            "Entering portalspace...")

        dest = self.db.dest

       # dest  = self.destination_position
        #print(self.destination)
        # user.location = self.destination_position
        print(dest)

        user.move_to(dest, move_type="teleport")

       # if self.dest:
            
        

        # new_stamina = round(user.stamina / 2)
        # user.update_vital('stamina', new_stamina)

    def at_post_use(self, user, **kwargs):

        # What happens when a player uses this?
        # dfdf

        pass
