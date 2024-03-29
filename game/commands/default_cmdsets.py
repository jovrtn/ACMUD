"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds

from . import general
from . import account
from . import door
from . import move

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.remove(default_cmds.CmdHome)
        self.remove(default_cmds.CmdSetHome)
        self.remove(default_cmds.CmdSetDesc)
        self.remove(default_cmds.CmdPose)
        self.remove(default_cmds.CmdNick)
        self.remove(default_cmds.CmdWhisper)
        self.remove(default_cmds.CmdDrop)
        self.remove(default_cmds.CmdSay)
        self.add(general.CmdLifestone)
        self.add(general.CmdTell)
        self.add(general.CmdChannel)
        self.add(general.CmdDrop)
        self.add(general.CmdUse)
        self.add(general.CmdEquip)
        self.add(general.CmdUnequip)
        self.add(general.CmdEquipment)
        self.add(door.DoorCmdSet)
        self.add(general.CmdAssess)
        self.add(general.CmdSay)
        self.add(general.CmdCast)
        self.add(general.CmdAttack)
        # self.add(move.MovementFailCmdSet)
  


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.remove(default_cmds.CmdDiscord2Chan)
        self.remove(default_cmds.CmdNick)
        self.remove(default_cmds.CmdPage)
        self.remove(default_cmds.CmdIC)
        self.remove(default_cmds.CmdOOC)
        self.remove(default_cmds.CmdCharCreate)
        self.remove(default_cmds.CmdChannel)
        self.add(account.CmdLogin)
        self.add(general.CmdLogout)
        self.add(account.CmdCreateChar)


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
