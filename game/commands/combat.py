import evennia

from commands.command import Command

from django.conf import settings
from evennia.utils import utils

from evennia import default_cmds


class CmdAttack(Command):
    """
    Attacks a target.

    Usage:
      attack <target>
      attack <target> <height>

    """
    key = "attack"
    help_category = "combat"

    def parse(self):
        self.args = self.args.strip()
        target, *attackHeight = self.args.split(" ", 1)
        self.target = target.strip()
        if attackHeight:
            self.attackHeight = attackHeight[0].strip()
        else:
            self.attackHeight = "medium"

    def func(self):
        if not self.args:
            self.caller.msg("Who do you want to attack?")
            return
        # get the target for the hit
        target = self.caller.search(self.target)
        if not target:
            return

        # get and handle the weapon
        # weapon = None
        # if self.weapon:
        #     weapon = self.caller.search(self.weapon)
        # if weapon:
        #     weaponstr = f"{weapon.key}"
        # else:
        #     weaponstr = "bare fists"

        # self.caller.msg(f"You hit {target.key} with {weaponstr}!")
        # target.msg(f"You got hit by {self.caller.key} with {weaponstr}!")


class CmdStopAttack(Command):
    """
    Stop attacking a target.

    Usage:
      stopattack

    """
    key = "stopattack"
    help_category = "combat"

    # def func(self):

    # Stop attack
