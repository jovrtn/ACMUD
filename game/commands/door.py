"""
Door

Contribution - Griatch 2016

A simple two-way exit that represents a door that can be opened and
closed. Can easily be expanded from to make it lockable, destroyable
etc.  Note that the Door is based on Evennia locks, so it will
not work for a superuser (which bypasses all locks) - the superuser
will always appear to be able to close/open the door over and over
without the locks stopping you. To use the door, use `@quell` or a
non-superuser account.

Installation:


Import this module in mygame/commands/default_cmdsets and add
the DoorCmdSet to your CharacterCmdSet:

```python
# in mygame/commands/default_cmdsets.py

from evennia.contrib.grid import Door  <---

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(Door.DoorCmdSet)

```

Usage:

To try it out, `dig` a new room and then use the (overloaded) `@open`
commmand to open a new doorway to it like this:

    @open doorway:contrib.grid.Door.Door = otherroom

You can then use `open doorway' and `close doorway` to change the open
state. If you are not superuser (`@quell` yourself) you'll find you
cannot pass through either side of the door once it's closed from the
other side.

"""

from evennia import DefaultExit, default_cmds
from evennia.commands.cmdset import CmdSet
from evennia.utils.utils import inherits_from

from typeclasses.exits import Door

class CmdOpen(default_cmds.CmdOpen):
    __doc__ = default_cmds.CmdOpen.__doc__
    # overloading parts of the default CmdOpen command to support doors.

    def create_exit(self, exit_name, location, destination, exit_aliases=None, typeclass=None):
        """
        Simple wrapper for the default CmdOpen.create_exit
        """
        # create a new exit as normal
        new_exit = super().create_exit(
            exit_name, location, destination, exit_aliases=exit_aliases, typeclass=typeclass
        )
        if hasattr(self, "return_exit_already_created"):
            # we don't create a return exit if it was already created (because
            # we created a door)
            del self.return_exit_already_created
            return new_exit
        if inherits_from(new_exit, Door):
            # a door - create its counterpart and make sure to turn off the default
            # return-exit creation of CmdOpen
            self.caller.msg(
                "Note: A door-type exit was created - ignored eventual custom return-exit type."
            )
            self.return_exit_already_created = True
            back_exit = self.create_exit(
                exit_name, destination, location, exit_aliases=exit_aliases, typeclass=typeclass
            )
            new_exit.db.return_exit = back_exit
            back_exit.db.return_exit = new_exit
        return new_exit


# A simple example of a command making use of the door exit class'
# functionality. One could easily expand it with functionality to
# operate on other types of open-able objects as needed.


class CmdOpenCloseDoor(default_cmds.MuxCommand):
    """
    Open and close a door

    Usage:
        open <door>
        close <door>

    """

    key = "open"
    aliases = ["close"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        "implement the door functionality"
        if not self.args:
            self.caller.msg("Usage: open||close <door>")
            return

        door = self.caller.search(self.args)
        if not door:
            return
        if not inherits_from(door, Door):
            self.caller.msg("This is not a door.")
            return

        if self.cmdstring == "open":
            if door.locks.check(self.caller, "traverse"):
                self.caller.msg("%s is already open." % door.key)
            else:
                door.setlock("traverse:true()")
                self.caller.msg("You open %s." % door.key)
        else:  # close
            if not door.locks.check(self.caller, "traverse"):
                self.caller.msg("%s is already closed." % door.key)
            else:
                door.setlock("traverse:false()")
                self.caller.msg("You close %s." % door.key)


class DoorCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdOpen())
        self.add(CmdOpenCloseDoor())