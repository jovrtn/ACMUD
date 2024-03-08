from evennia import default_cmds, CmdSet

class CmdExitError(default_cmds.MuxCommand):
    """Parent class for all exit-errors."""
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    auto_help = False
    def func(self):
        """Returns error based on key"""
        self.caller.msg(f"You cannot move {self.key}.")

class CmdExitErrorNorth(CmdExitError):
    key = "north"
    aliases = ["n"]

class CmdExitErrorEast(CmdExitError):
    key = "east"
    aliases = ["e"]

class CmdExitErrorSouth(CmdExitError):
    key = "south"
    aliases = ["s"]

class CmdExitErrorWest(CmdExitError):
    key = "west"
    aliases = ["w"]

# you could add each command on its own to the default cmdset,
# but putting them all in a cmdset here allows you to
# just add this and makes it easier to expand with more 
# exit-errors in the future

class MovementFailCmdSet(CmdSet):
    def at_cmdset_creation(self): 
        self.add(CmdExitErrorNorth())
        self.add(CmdExitErrorEast())
        self.add(CmdExitErrorWest())
        self.add(CmdExitErrorSouth()) 