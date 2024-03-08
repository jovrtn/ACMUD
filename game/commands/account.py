from evennia import default_cmds

import evennia

from commands.command import Command

from django.conf import settings
from evennia.utils import utils


from world.chargen import start_chargen

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


class CmdLogin(default_cmds.CmdIC):
    """
    control an object you have permission to puppet

    Usage:
      login <character>

    Log into the game as a given character.

    This will attempt to "become" a different object assuming you have
    the right to do so. Note that it's the ACCOUNT character that puppets
    characters/objects and which needs to have the correct permission!

    You cannot become an object that is already controlled by another
    account. In principle <character> can be any in-game object as long
    as you the account have access right to puppet it.
    """

    key = "login"

    def func(self):
        super().func()

class CmdCreateChar(COMMAND_DEFAULT_CLASS):
    """
    create a new character

    Usage:
      createchar <charname>

    Create a new character
    """

    key = "createchar"
    locks = "cmd:pperm(Player)"
    help_category = "General"

    # this is used by the parent
    account_caller = True

    def func(self):
        """create the new character"""
        account = self.account

        print("CmdCreateCar")

        print(self.caller)
        #print(self.session)
        
        if not self.args:
            self.msg("Usage: createchar")
            return


        start_chargen(self.caller, self.session)


        # key = self.lhs
        # description = self.rhs or "This is a character."





        # new_character, errors = self.account.create_character(
        #     key=key, description=description, ip=self.session.address
        # )

        # if errors:
        #     self.msg(errors)
        # if not new_character:
        #     return

        # self.msg(
        #     f"Created new character {new_character.key}. Use |wlogin {new_character.key}|n to log in to the game."
        # )
