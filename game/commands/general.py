# from  import Command
# from evennia import CmdSet
# from evennia import default_cmds

# from evennia.commands.command import Command as BaseCommand
# from evennia.commands.default import muxcommand as MuxCommand

# from rich.console import Console
from evennia.commands.default.comms import CmdObjectChannel
from enums import WeeniePropInt, WeeniePropBool, ItemType, BondedStatus, EquipMask, EquipSlot, EquipSlotMask
from evennia import default_cmds
from evennia.utils import utils, evtable, evform
from django.conf import settings
from commands.command import Command, OnCommand
import evennia
from io import StringIO
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.tree import Tree

from rich.console import Group

from rich.layout import Layout

from rich import box

import time

SPELL_ALIASES = {
    "str1": 2,
    "end1": 1349
}

SPELLS = [{
    "key": 2,
    "value": {
        "base_mana": 15,
        "base_range_constant": 0.0,
        "base_range_mod": 0.0,
        "bitfield": 16396,
        "caster_effect": 0,
        "category": 1,
        "component_loss": 0.01,
        "desc": "Increases the caster's Strength by 10 points.",
        "display_order": 10426,
        "fizzle_effect": 0,
        "formula": [1, 7, 33, 44, 60, 0, 0, 0],
        "formula_version": 1,
        "iconID": 100668300,
        "mana_mod": 0,
        "name": "Strength Self I",
        "non_component_target_type": 16,
        "power": 1,
        "recovery_amount": 0.0,
        "recovery_interval": 0.0,
        "school": 4,
        "spell_economy_mod": 1.0,
        "target_effect": 6,
        "meta_spell": {
            "sp_type": 1,
            "spell": {
                "spell_id": 2,
                "degrade_limit": -666.0,
                "degrade_modifier": 0.0,
                "duration": 1800.0,
                "smod": {"key": 1, "type": 36865, "val": 10.0},
                "spellCategory": 1
            }
        }
    },
    "lastModified": "2020-07-24T14:00:37.6543596-05:00",
    "modifiedBy": "Morosity",
    "changelog": [],
    "isDone": False
}, {"key": 1349, "value": {"base_mana": 15, "base_range_constant": 0.0, "base_range_mod": 0.0, "bitfield": 16398, "caster_effect": 0, "category": 3, "component_loss": 0.01, "desc": "Increases the caster's Endurance by 10 points.", "display_order": 2504, "fizzle_effect": 0, "formula": [1, 7, 33, 48, 60, 0, 0, 0], "formula_version": 1, "iconID": 100668273, "mana_mod": 0, "name": "Endurance Self I", "non_component_target_type": 16, "power": 1, "recovery_amount": 0.0, "recovery_interval": 0.0, "school": 4, "spell_economy_mod": 1.0, "target_effect": 10, "meta_spell": {"sp_type": 1, "spell": {"spell_id": 1349, "degrade_limit": -666.0, "degrade_modifier": 0.0, "duration": 1800.0, "smod": {"key": 2, "type": 36865, "val": 10.0}, "spellCategory": 3}}}, "lastModified": "2020-07-24T14:00:50.9710677-05:00", "modifiedBy": "Morosity", "changelog": [], "isDone": False}]

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


def includes_flag(val, flag):
    return val & flag == val


class CmdChannel(CmdObjectChannel):
    pass


class CmdLifestone(COMMAND_DEFAULT_CLASS):
    """
    recall to the last lifestone you attuned with

    Usage:
      lifestone

    Recall to your attuned lifestone.
    """

    key = "lifestone"
    # locks = "cmd:perm(home) or perm(Builder)"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        home = caller.home
        if not home:
            # caller.msg("You have no home!")
            return
        elif home == caller.location:
            return
            # caller.msg("You are already home!")
        else:
            caller.location.msg_contents(
                "|g{player} is recalling to the lifestone.|n", mapping={"player": caller})
            caller.move_to(home, move_type="teleport")


class CmdTell(COMMAND_DEFAULT_CLASS):
    """
    Speak privately as your character to another

    Usage:
      tell <character> = <message>

    Talk privately to a character anywhere in the world.
    """

    key = "tell"
    locks = "cmd:all()"

    def func(self):
        """Run the tell command"""

        caller = self.caller

        if not self.lhs or not self.rhs:
            caller.msg("Usage: tell <character> <message>")
            return

        receivers = caller.search(
            self.lhs.strip(), quiet=True, global_search=True)

        print(receivers)

        if not receivers:
            caller.msg("That person is not available now.")

        speech = self.rhs
        # If the speech is empty, abort the command
        if not speech or not receivers:
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_pre_say(speech, whisper=True, receivers=receivers,
                                   msg_receivers='{object} tells you, "|n{speech}|n"')

        # no need for self-message if we are whispering to ourselves (for some reason)
        # msg_self = None if caller in receivers else True
        # caller.at_say(speech, msg_self=msg_self,
        #               receivers=receivers, whisper=True)

        if caller in receivers:
            print('Caller is in receivers')
            caller.at_say(speech, msg_self=None,
                          receivers=receivers, whisper=True, msg_receivers='You think, "|n{speech}|n"')

        else:
            caller.at_say(speech, msg_self='{self} tell {all_receivers}, "|n{speech}|n"',
                          receivers=receivers, whisper=True)


# class MyCmdSet(CmdSet):

#     def at_cmdset_creation(self):
#         self.add(CmdEcho)

class CmdLogout(default_cmds.CmdOOC):
    """
    control an object you have permission to puppet

    Usage:
      logout

    Exit to the character selection menu
    """

    key = "logout"

    def func(self):
        super().func()


class CmdEquip(Command):
    """
    equip an item to a slot

    Usage:
      equip <item>
      equip <item> <slot>

    Exit to the character selection menu
    """

    key = "equip"

    def parse(self):
        """
        Handle parsing of most supported combat syntaxes (except stunts).

        <action> <item>
        or
        <action> <item> [to] <slot>

        Use 'to' to differentiate if names/items have spaces in the name.

        """

        self.args = args = self.args.strip()
        self.lhs, self.rhs = "", ""

        print('CmdEquip')
        print(args)

        if not args:
            return

        if " to " in args:
            lhs, rhs = args.split(" to ")
        else:
            lhs = args
            # rhs = " ".join(rhs)
        self.lhs = lhs.strip()

    def func(self):

        print(self.lhs)
        if self.caller.at_pre_equip(self.lhs):
            self.caller.at_equip(self.lhs)
            self.caller.at_post_equip(self.lhs)


class CmdUnequip(Command):
    """
    equip an item to a slot

    Usage:
      unequip <item>
      unequip <item> from <slot>

    Exit to the character selection menu
    """

    key = "unequip"

    def parse(self):
        """
        Handle parsing of most supported combat syntaxes (except stunts).

        <action> <item>
        or
        <action> <item> [from] <slot>

        Use 'from' to differentiate if names/items have spaces in the name.

        """

        self.args = args = self.args.strip()
        self.lhs, self.rhs = "", ""

        print('CmdEquip')
        print(args)

        if not args:
            return

        if " from " in args:
            lhs, rhs = args.split(" from ")
        else:
            lhs = args
            # rhs = " ".join(rhs)
        self.lhs = lhs.strip()

    def func(self):

        print(self.lhs)
        self.caller.unequip(self.lhs)


class CmdCast(OnCommand):
    """
    Casts a spell.

    Usage:
      cast <spell>
      cast <spell> on <target>

    """
    key = "cast"
    help_category = "Magic"

    def func(self):

        if not self.args:
            self.caller.msg("Which spell do you want to cast?")
            return

        # Check for combat handler on caster
        # If found, run through self/target checks and insert spell into combat action queue
        # If not found, run through checks and proceed

        # If no target, check if spell can be cast on self
        # If it can, proceed with cast
        # If it cannot, return with error text

        # Check if spell can be cast on self
        # If no, it needs a target
        # Check if spell can be cast on target type
        # If no, return with error message

        # get the target for the hit

        # find spell

        print(self.lhs)

        spell = None

        if self.lhs in SPELL_ALIASES:

            # Spell command exists, looking up spell

            spell_id = SPELL_ALIASES[self.lhs]
            spell = next((x for x in SPELLS if x["key"] == spell_id), None)
        else:
            # Spell alias could not be found, send error message
            self.caller.msg("No spell found")
            return

        if not spell:
            # Send message that the spell could not be found
            self.caller.msg("No spell found")
            return

        # Spell is found, proceed

        print(spell)

        # Check if the spell can have a target

        # target = self.caller.search(self.rhs)
        duration = 20
        expires_at = int(time.time()) + duration

        self.caller.enchantments.add(self.caller, spell, expires_at)

        # If spell can't have a target, and a target exists on the input, send warning message

        # If spell can have a target:

        # Check if there is a target

        # Check if target is valid type for this spell

        # Check if spell requires a target

        # if not target:
        #     return

        # If spell is harmful, c


class CmdDrop(COMMAND_DEFAULT_CLASS):
    """
    drop something

    Usage:
      drop <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("What do you want to drop?")
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller

        obj = caller.search(
            self.args,
            candidates=self.caller.contents,
            nofound_string=f"You aren't carrying {self.args}.",
            multimatch_string=f"You carry more than one {self.args}:",
        )
        if not obj:
            return

        # Call the object script's at_pre_drop() method.
        if not obj.at_pre_drop(caller):
            return

        success = obj.move_to(caller.location, quiet=True, move_type="drop")
        if not success:
            caller.msg("This couldn't be dropped.")
        else:
            singular, _ = obj.get_numbered_name(1, caller)
            caller.location.msg_contents(
                f"$You() $conj(drop) {singular}.", from_obj=caller)
            # Call the object script's at_drop() method.
            obj.at_drop(caller)


class CmdUse(Command):
    """
    Use or activate an item.

    Usage:
      use <target>
      use <item>
      use <item> on <item>

    An item can have various function - looking at the item may
    provide information as to its effects.
    """

    key = "use"
    # aliases = ["activate"]
    help_category = "General"

    def parse(self):
        """
        Handle parsing of most supported combat syntaxes (except stunts).

        <action> [<target>|<item>]
        or
        <action> <item> [on] <target>

        Use 'on' to differentiate if names/items have spaces in the name.

        """

        self.args = args = self.args.strip()
        self.lhs, self.rhs = "", ""

        print('CmdUse')
        print(args)

        if not args:
            return

        if " on " in args:
            lhs, rhs = args.split(" on ", 1)
        else:
            lhs = args
            # rhs = " ".join(rhs)
        self.lhs = lhs.strip()

        # self.args = self.args.strip()
        # target, *target2 = self.args.split(" on ", 1)
        # if not target2:
        #     target, *weapon = target.split(" ", 1)
        # self.target = target.strip()
        # if weapon:
        #     self.weapon = weapon[0].strip()
        # else:
        #     self.weapon = ""

        # # Check for 'on' string

        # target, *args = self.args.split()

        # self.item = None
        # self.target_item = None

        # self.target = None

    def func(self):
        """
        This performs the actual command.
        """

        # inventory_contents = self.caller.get_all_contents()

        item = self.caller.search(self.lhs)

        # item = self.caller.search(self.lhs)

        # Search inventory for left-hand item

        # If left-hand is in inventory, do extra checks

        # If "on" found, ensure left-hand item is inventory

        # if not item

        if (item):
            item.use(self.caller)

        # target = None

    # def func(self):
    #     super().func()


class CmdEquipment(Command):
    """
    Use or activate an item.

    Usage:
      use <target>
      use <item>
      use <item> on <item>

    An item can have various function - looking at the item may
    provide information as to its effects.
    """

    key = "equipment"
    aliases = ["eq", "worn", "gear"]
    help_category = "General"

    def func(self):
        """
        This performs the actual command.
        """

        # slots = {
        #     "main_hand": {
        #         "label": "Main Hand"
        #     },
        #     "off_hand": {
        #         "Off Hand/Shield"
        #     },
        # }

        slots = {
            EquipSlot.MainHand: {
                "label": "Main Hand",
                "locations": [EquipMask.MissileWeapon, EquipMask.MeleeWeapon, EquipMask.Held, EquipMask.TwoHanded]
            },
            EquipSlot.OffHand: {
                "label": "Off Hand / Shield",
                "locations": [EquipMask.MissileWeapon, EquipMask.Held, EquipMask.TwoHanded, EquipMask.Shield]
            },
            EquipSlot.Head: {
                "label": "Head",
                "locations": [EquipMask.HeadWear]
            },
            EquipSlot.Chest: {
                "label": "Chest",
                "locations": [EquipMask.ChestArmor]
            },
            EquipSlot.UpperArm: {
                "label": "Upper Arms",
                "locations": [EquipMask.UpperArmArmor]
            },
            EquipSlot.LowerArm: {
                "label": "Lower Arms",
                "locations": [EquipMask.LowerArmArmor]
            },
            EquipSlot.Abdomen: {
                "label": "Abdomen",
                "locations": [EquipMask.AbdomenArmor]
            },
            EquipSlot.Hands: {
                "label": "Hands",
                "locations": [EquipMask.HandWear]
            },
            EquipSlot.UpperLeg: {
                "label": "Upper Legs",
                "locations": [EquipMask.UpperLegArmor]
            },
            EquipSlot.LowerLeg: {
                "label": "Lower Legs",
                "locations": [EquipMask.LowerLegArmor]
            },
            EquipSlot.Feet: {
                "label": "Feet",
                "locations": [EquipMask.FootWear]
            },
            EquipSlot.SigilOne: {
                "label": "Blue Sigil",
                "locations": [EquipMask.SigilOne]
            },
            EquipSlot.SigilTwo: {
                "label": "Yellow Sigil",
                "locations": [EquipMask.SigilTwo]
            },
            EquipSlot.SigilThree: {
                "label": "Red Sigil",
                "locations": [EquipMask.SigilThree]
            },
            EquipSlot.Neck: {
                "label": "Neck",
                "locations": [EquipMask.NeckWear]
            },
            EquipSlot.Trinket: {
                "label": "Trinket",
                "locations": [EquipMask.TrinketOne]
            },
            EquipSlot.WristLeft: {
                "label": "Wrist 1",
                "locations": [EquipMask.WristWearLeft]
            },
            EquipSlot.WristRight: {
                "label": "Wrist 2",
                "locations": [EquipMask.WristWearRight]
            },
            EquipSlot.FingerLeft: {
                "label": "Finger 1",
                "locations": [EquipMask.FingerWearLeft]
            },
            EquipSlot.FingerRight: {
                "label": "Finger 2",
                "locations": [EquipMask.FingerWearRight]
            },
            EquipSlot.Cloak: {
                "label": "Back",
                "locations": [EquipMask.Cloak]
            },
            EquipSlot.Shirt: {
                "label": "Shirt",
                "locations": [EquipMask.UpperArmWear, EquipMask.ChestWear, EquipMask.LowerArmWear, EquipMask.AbdomenWear]
            },
            EquipSlot.Pants: {
                "label": "Pants",
                "locations": [EquipMask.UpperLegWear, EquipMask.LowerLegWear, EquipMask.LowerArmWear]
            },
            EquipSlot.Ammunition: {
                "label": "Ammunition",
                "locations": [EquipMask.MissileAmmo]
            }
        }

        slot_types = {
            "Weapons": [EquipSlot.MainHand, EquipSlot.OffHand, EquipSlot.Ammunition],
            "Armor": [EquipSlot.Head, EquipSlot.MainHand.Chest, EquipSlot.UpperArm, EquipSlot.LowerArm, EquipSlot.Abdomen, EquipSlot.MainHand.Hands, EquipSlot.UpperLeg, EquipSlot.LowerLeg, EquipSlot.Feet],
            "Jewelry": [EquipSlot.Neck, EquipSlot.Trinket, EquipSlot.WristLeft, EquipSlot.WristRight, EquipSlot.FingerLeft, EquipSlot.FingerRight],
            "Clothing": [EquipSlot.Cloak, EquipSlot.Shirt, EquipSlot.Pants],
        }

        slot_items = {
            EquipSlot.MainHand: None,
            EquipSlot.OffHand: None,
            EquipSlot.Head: None,
            EquipSlot.Chest: None,
            EquipSlot.UpperArm: None,
            EquipSlot.LowerArm: None,
            EquipSlot.Abdomen: None,
            EquipSlot.Hands: None,
            EquipSlot.UpperLeg: None,
            EquipSlot.LowerLeg: None,
            EquipSlot.Feet: None,
            EquipSlot.SigilOne: None,
            EquipSlot.SigilTwo: None,
            EquipSlot.SigilThree: None,
            EquipSlot.Neck: None,
            EquipSlot.Trinket: None,
            EquipSlot.WristLeft: None,
            EquipSlot.WristRight: None,
            EquipSlot.FingerLeft: None,
            EquipSlot.FingerRight: None,
            EquipSlot.Cloak: None,
            EquipSlot.Shirt: None,
            EquipSlot.Pants: None,
            EquipSlot.Ammunition: None
        }

        equipped_items = self.caller.equipped_items

        # for equipped_item in equipped_items:

        #     pass
        # if includes_flag(equipped_item.locations_int,

        # if ()

        inventory_contents = self.caller.get_inventory()

        console = Console(file=StringIO(), color_system="256")
        empty_text = Text("Empty", style="grey27")
        tables = {}

        for key, value in slot_types.items():
            table = Table(show_lines=True, expand=True, box=box.ASCII2,
                          header_style="bold dark_goldenrod", border_style="orange4")
            table.add_column(key, no_wrap=True, justify="center")
            # table.add_row(table2)
            child_table = Table(show_lines=True, expand=True, show_header=False, show_edge=False, pad_edge=False,
                                leading=0, box=box.ASCII2, header_style="bold dark_goldenrod", border_style="orange4")
            child_table.add_column(ratio=2)
            child_table.add_column(ratio=4)

            for slot in value:

                slot_label = slots[slot]["label"]
                label_text = Text(slot_label, style="orange4")
                item_text = empty_text
                slot_item = slot_items[slot]

                if slot_item:
                    item_text = Text(slot_item.name, style="white")

                # if slot == "Cloak":
                #     item_text = Text("Silk Cloak (5)", style="dodger_blue1")
                # elif slot == "Trinket":
                #     item_text = Text("Pathwarden Trinket", style="dodger_blue1")
                # elif slot == "Chest" or slot == "Upper Arms" or slot =="Lower Arms" or slot == "Abdomen":
                #     item_text = Text("Mattekar Hide Coat", style="white")
                # elif slot == "Head":
                #     item_text = Text("Olthoi Helm", style="white")
                # elif slot == "Necklace":
                #     item_text = Text("Baron's Amulet of Life Giving", style="dodger_blue1")

                child_table.add_row(label_text, item_text)

            table.add_row(child_table)
            tables[key] = table

        left_col_group = Group(
            tables["Armor"],
        )

        right_col_group = Group(
            tables["Jewelry"],
            tables["Clothing"]
        )

        aetheria_table = Table(show_lines=True, expand=True, box=box.ASCII2,
                               header_style="bold dark_goldenrod", border_style="orange4")
        aetheria_table.add_column("Aetheria", no_wrap=True, justify="center")
        aetheria_child_table = Table(show_lines=True, expand=True, show_header=False, show_edge=False,
                                     pad_edge=False, leading=0, box=box.ASCII2, header_style="bold dark_goldenrod", border_style="orange4")
        aetheria_blue_text = Text("Defense (3)", style="bright_blue")
        aetheria_yellow_text = Text("Defense (5)", style="bright_yellow")
        aetheria_red_text = Text("Destruction (5)", style="bright_red")
        aetheria_child_table.add_column(justify="center", ratio=1)
        aetheria_child_table.add_column(justify="center", ratio=1)
        aetheria_child_table.add_column(justify="center", ratio=1)
        aetheria_child_table.add_row(
            aetheria_blue_text, aetheria_yellow_text, aetheria_red_text)
        aetheria_table.add_row(aetheria_child_table)

        weapons_table = Table(show_lines=True, expand=True, box=box.ASCII2,
                              header_style="bold dark_goldenrod", border_style="orange4")
        weapons_table.add_column(
            "Off Hand / Shield", ratio=1, no_wrap=True, justify="center")
        weapons_table.add_column("Main Hand", ratio=1,
                                 no_wrap=True, justify="center")
        weapons_table.add_column(
            "Ammunition", ratio=1, no_wrap=True, justify="center")

        main_hand_text = empty_text
        off_hand_text = empty_text
        ammunition_text = empty_text

        main_hand_item = slot_items[EquipSlot.MainHand]
        off_hand_item = slot_items[EquipSlot.OffHand]
        ammunition_item = slot_items[EquipSlot.Ammunition]

        if main_hand_item:
            main_hand_text = Text(main_hand_item.name, style="white")
        if off_hand_item:
            off_hand_text = Text(off_hand_item.name, style="white")
        if ammunition_item:
            ammunition_text = Text(ammunition_item.name, style="white")

        weapons_table.add_row(off_hand_text, main_hand_text, ammunition_text)

        # Grids

        grid_top = Table(show_lines=False, show_edge=False, expand=True,
                         show_header=False, padding=(0, 0, 0, 1), safe_box=True, box=None)
        grid_top.add_column(justify="center")
        grid_top.add_row(aetheria_table)

        grid_mid = Table(show_lines=False, show_edge=False, expand=True,
                         show_header=False, padding=(0, 0, 0, 1), safe_box=True, box=None)
        grid_mid.add_column(ratio=1)
        grid_mid.add_column(justify="right", ratio=1)
        grid_mid.add_row(left_col_group, right_col_group)

        grid_bot = Table(show_lines=False, show_edge=False, expand=True,
                         show_header=False, padding=(0, 0, 0, 1), safe_box=True, box=None)
        grid_bot.add_column(justify="center")
        grid_bot.add_row(weapons_table)

        # Main Table

        table = Table(expand=True, box=box.ASCII2, padding=(
            0, 1, 0, 0), header_style="bold dark_goldenrod", border_style="orange4")
        table.add_column("Equipment", justify="center")
        table.add_row(grid_top)
        table.add_row(grid_mid)
        table.add_row(grid_bot)

        # Send Message

        console.print(table)
        str_output = console.file.getvalue()
        self.caller.msg(str_output)
        self.caller.msg(equipped_items)

    # def func(self):
    #     super().func()


class CmdAssess(Command):
    """
    Use or activate an item.

    Usage:
      assess <target>
      assess <item>

    An item can have various function - looking at the item may
    provide information as to its effects.
    """

    key = "assess"
    # aliases = ["eq", "worn", "gear"]
    help_category = "General"

    def parse(self):
        """
        Handle parsing of most supported combat syntaxes (except stunts).

        <action> <item>
        or
        <action> <item> [to] <slot>

        Use 'to' to differentiate if names/items have spaces in the name.

        """

        self.args = args = self.args.strip()
        # self.lhs, self.rhs = "", ""

        lhs = args
        self.lhs = lhs.strip()

    def func(self):
        """
        This performs the actual command.
        """

        target = self.caller.search(self.lhs)

        if (target):

            self.caller.msg('Examining: ' + target.name)


class CmdSay(default_cmds.CmdSay):
    """
    speak as your character

    Usage:
      say <message>

    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    # don't require a space after `say/'/"`
    arg_regex = None

    def func(self):
        """Run the say command"""

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        speech = self.args

        # Calling the at_pre_say hook on the character
        speech = caller.at_pre_say(speech)

        # If speech is empty, stop here
        if not speech:
            return

        if speech.lower() == "Malar Cazael".lower():
            speech = f"|b{speech}|n"
            pass

        # Call the at_post_say hook on the character
        caller.at_say(speech, msg_self=True)






class CmdAttack(Command):
    """
    Use or activate an item.

    Usage:
      attack <target>

    An item can have various function - looking at the item may
    provide information as to its effects.
    """

    key = "attack"
    # aliases = ["eq", "worn", "gear"]
    help_category = "Combat"

    def parse(self):
        """
        Handle parsing of most supported combat syntaxes (except stunts).

        <action> <target>

        """

        self.args = args = self.args.strip()
        self.lhs = args.strip()

    def func(self):
        """
        This performs the actual command.
        """

        print("Attack command")

        # Prefilter room for potential attackables

        current_room = self.caller.location
        room_contents = current_room.contents

        print("Room contents")
        print(room_contents)

        attackable_objects = []

        for item in room_contents:
            attackable = item.attributes.get(WeeniePropBool.Attackable.value, default=False, category="properties")
            if attackable: attackable_objects.append(item)

        print("Attackable objects")
        print(attackable_objects)

        target = self.caller.search(self.lhs, candidates=attackable_objects, multimatch_string="test multimatch")

        if target:
            print(target)

            target.combat_target = self.caller
            self.caller.attack(target)
     