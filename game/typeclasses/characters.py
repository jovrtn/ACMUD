"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter
from typeclasses.creatures import Creature
from evennia.typeclasses.attributes import AttributeProperty
from enums import EquipMask, WeeniePropInt, EquipSlotMask, EquipSlot


def has_flag(val, flag):
    return val & flag == flag


def includes_flag(val, flag):
    return val & flag == val


SKILL_CREDITS_CREATION = 52


class Character(Creature, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the prelogout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    prelogout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    name_color = "|W"
    # pk_flagged = AttributeProperty(default=False)
    # pkl_flagged = AttributeProperty(default=False)

    # skill_credits = AttributeProperty(default=SKILL_CREDITS_CREATION)

    # corpse_location = AttributeProperty(default=None, autocreate=False)
    # last_pk_combat = AttributeProperty(default=None, autocreate=False)

    # linked_lifestone = AttributeProperty(default=None, autocreate=False)
    # linked_portal_one = AttributeProperty(default=None, autocreate=False)
    # linked_portal_two = AttributeProperty(default=None, autocreate=False)

    # add support for natural resistances based on strength, endurance, etc

    def equip(self, lhs, **kwargs):
        if self.at_pre_equip(lhs):
            self.at_equip(lhs)
            self.at_post_equip(lhs)

    def at_pre_equip(self, lhs, **kwargs):

        if not lhs:
            self.msg("What do you want to equip?")
            return False

        return True

    def at_equip(self, lhs, **kwargs):

        all_inventory = self.get_all_inventory()

        items = self.search(lhs, quiet=True, candidates=all_inventory)

        print(items)

        if len(items) == 0:
            self.msg("That item is not in your inventory.")

        elif len(items) > 1:
            self.msg("Which item do you want to equip?")

        else:

            item = items[0]

            item_locations = item.attributes.get(
                'locations_int',
                category="properties"
            )

            items_to_unequip = []

            equip_msgs = []

            equip_error_msgs = []

            equip_item = False
            equip_locations = item_locations

            equipped_items = self.attributes.get("equipped_items", {})

            # Check if ring or bracelet

            print(item_locations)

            if includes_flag(item_locations, EquipMask.FingerWear):

                print('Check rings')

                if EquipMask.FingerWearLeft in equipped_items and EquipMask.FingerWearRight in equipped_items:
                    equip_msgs.append(
                        "You're already wearing jewelry on both hands.")
                elif EquipMask.FingerWearLeft not in equipped_items:
                    equip_msgs.append(
                        f"You equip {item.name} to your right finger.")
                    equip_item = True
                    equip_locations = EquipMask.FingerWearLeft.value
                else:
                    equip_msgs.append(
                        f"You equip {item.name} to your left finger.")
                    equip_item = True
                    equip_locations = EquipMask.FingerWearRight.value

            elif includes_flag(item_locations, EquipMask.WristWear):

                print('Check bracelets')

                if EquipMask.WristWearLeft in equipped_items and EquipMask.WristWearRight in equipped_items:
                    equip_msgs.append(
                        "You're already wearing jewelry on both wrists.")
                elif EquipMask.WristWearLeft not in equipped_items:
                    equip_msgs.append(
                        f"You equip {item.name} to your right wrist.")
                    equip_item = True
                    equip_locations = EquipMask.WristWearLeft.value
                else:
                    equip_msgs.append(
                        f"You equip {item.name} to your left wrist.")
                    equip_item = True
                    equip_locations = EquipMask.WristWearRight.value

            elif includes_flag(item_locations, EquipSlotMask.Ammunition):

                print('Check Ammo')

        
                if EquipSlotMask.Ammunition in equipped_items:
                    self.unequip(equipped_items[EquipSlotMask.Ammunition].name)

                
                equip_item = True
            
                

                             

            elif includes_flag(item_locations, EquipSlotMask.OffHand):

                print('Check Offhand')

                can_wield = True

                for key, value in equipped_items.items():
                    if includes_flag(key, EquipMask.TwoHanded | EquipMask.MissileWeapon | EquipMask.Held):
                        can_wield = False
                        equip_msgs.append(f"{item.name} cannot be used with {value.name}")
                        break
                
                if can_wield:
                    #equip_msgs.append(f"You equip {item.name} to your off hand.")
                    equip_item = True
                    equip_locations = EquipSlotMask.OffHand.value              

            elif includes_flag(item_locations, EquipMask.MeleeWeapon | EquipMask.TwoHanded | EquipMask.MissileWeapon | EquipMask.Held):

                print("MAIN HAND CHECK")

                uses_both_hands = includes_flag(
                    item_locations, EquipMask.TwoHanded | EquipMask.MissileWeapon | EquipMask.Held)

                for equipped_item_key in equipped_items.keys():

                    if includes_flag(equipped_item_key, EquipMask.TwoHanded | EquipMask.MissileWeapon | EquipMask.Held | EquipMask.MeleeWeapon):
                        main_hand_equipped = equipped_items[equipped_item_key]
                        self.unequip(main_hand_equipped.name)

                if uses_both_hands and EquipSlotMask.OffHand in equipped_items:
                    off_hand_equipped = equipped_items[EquipSlotMask.OffHand]
                    self.unequip(off_hand_equipped.name)
                    #equip_msgs.append(f"You unwield {off_hand_equipped.name}.")

                #equip_msgs.append(f"You wield {item.name}.")
                equip_item = True
                equip_locations = item_locations

            else:
  
                can_wield = True
                for key, value in equipped_items.items():
                    if includes_flag(item_locations, key):
                        can_wield = False
                        equip_msgs.append(f"You must remove your {value.name} to wear that")
                        break

                if can_wield:
                    equip_item = True


            if equip_item:
                print("If there's an item to equip:")
                equipped_items = self.attributes.get("equipped_items", {})
                
                print(equip_locations)
                print(item)
                equipped_items[equip_locations] = item
                equip_msgs.append(f"You equip {item.name}")
                self.attributes.add("equipped_items", equipped_items)

            for msg in equip_msgs:
                self.msg(msg)

        pass

    def unequip(self, lhs, **kwargs):
        if self.at_pre_unequip(lhs):
            self.at_unequip(lhs)
            self.at_post_unequip(lhs)

    def at_post_equip(self, item, **kwargs):
        pass

    def at_pre_unequip(self, item, **kwargs):

        if not item:
            self.msg("What do you want to unequip?")
            return False

        return True

    def at_unequip(self, item, **kwargs):

        print('at_unequip')

        equipped_items = self.get_equipped()

        items = self.search(item, quiet=True, candidates=equipped_items)

        print(items)

        if len(items) == 0:
            self.msg("You don't have that item equipped.")

        elif len(items) > 1:
            self.msg("Which item do you want to unequip?")

        else:

            item = items[0]
            equipped_items = self.attributes.get("equipped_items", {})

            item_key = None
            for key, value in equipped_items.items():
                if value == item:
                    item_key = key
                    break

            # item = items[0]
            # locations = item.attributes.get(
            #     'locations_int',
            #     category="properties"
            # )

            print("Equipped items:")
            print(equipped_items)

            print('Deleting item from equipped_items with key:')
            print(item_key)

            del equipped_items[item_key]

            self.attributes.add("equipped_items", equipped_items)

            # self.db.equipped_items[locations] = item

            self.msg(f"You unequip {item.name}")
            print(equipped_items)

        pass

    def at_post_unequip(self, item, **kwargs):
        pass
