
from evennia.utils.utils import lazy_property, repeat, delay
from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty
from handlers.inventory import InventoryHandler
from handlers.attributes import AttributesHandler
from handlers.vitals import VitalsHandler
from handlers.enchantments import EnchantmentsHandler

from evennia import create_script


from evennia.prototypes import prototypes, spawner

from enums import ItemType, WeeniePropIID, CreaturePose

from typeclasses.containers import Container

from typeclasses.objects import Object

from evennia import TICKER_HANDLER as tickerhandler


import random

MIN_ATTRIBUTE_VALUE = 10
MAX_XP = 191226310247
MIN_XP = 0


class Creature(Object):
    """
    This is a base class for Creatures.
    """

    pose = CreaturePose.Standing
    equipped_items = AttributeProperty(default={}, autocreate=False)
    attacking = False
    repeat_attack = True

    @lazy_property
    def attribs(self):
        return AttributesHandler(self)

    @lazy_property
    def vitals(self):
        return VitalsHandler(self)

    @lazy_property
    def enchantments(self):
        return EnchantmentsHandler(self)

    @property
    def is_player(self):
        return self.is_typeclass('typeclasses.characters.Character')

    @property
    def is_alive(self):
        return self.vitals.health.current > 0

    def at_heartbeat(self):

        # check if vitals are below 0 first?
        self.vitals.regen()

        # Improve this to check if there are any enchantments that have expirations set first?
        if self.enchantments.all:
            self.enchantments.check_expired()

        # check expired buffs

    def at_object_creation(self):
        tickerhandler.add(5, self.at_heartbeat)

        # Set current vitals to max value
        # self.vitals.update_vital("health", self.vitals.health.data["current_Level"] or self.vitals.health.max)
        # self.vitals.update_vital("stamina", self.vitals.stamina.data["current_Level"] or self.vitals.stamina.max)
        # self.vitals.update_vital("mana", self.vitals.mana.data["current_Level"] or self.vitals.mana.max)

        # create_script(key="npc_combat",
        #               interval=2,  # seconds <=0 means off
        #               start_delay=False,  # wait interval before first call
        #               # start timer (else needing .start() )
        #               autostart=False,
        #               typeclass="typeclasses.scripts.NPCCombatScript", obj=self)

        # self.scripts.add(npc_combat_script)

        # print(self.scripts)

    def at_object_delete(self):

        # Clean up tickers

        # tickerhandler.remove(5, self.at_heartbeat)

        # Clean up child objects

        all_child_objects = self.get_inventory() + self.get_equipped() + \
            self.get_containers()

        for item in all_child_objects:
            item.delete()

        return True

    def get_equipped(self):
        equipped = self.attributes.get('equipped_items', {})
        return list(equipped.values()) if equipped else []

    def get_backpack_contents(self):
        contents = self.contents
        equipped = self.get_equipped()
        backpack_items = [
            item for item in contents if item not in equipped and not isinstance(item, Container)]
        return backpack_items

    def get_inventory(self):

        all_contents = []
        contents = self.contents
        equipped = self.get_equipped()

        for item in contents:
            if (item.is_typeclass("typeclasses.containers.Container")):
                for nested_item in item.contents:
                    all_contents.append(nested_item)
            else:
                all_contents.append(item)

        all_inventory = [item for item in all_contents if item not in equipped]

        return all_inventory

    def get_containers(self):
        return [item for item in self.contents if item.is_typeclass("typeclasses.containers.Container")]

    def at_pre_object_receive(self, moved_object, source_location, **kwargs):

        # Validate that an object can be received here

        # Loop through every pack container to find space

        print("at_pre_object_receive")

        # check if object is container

        # if object container, put in inventory.containers.packs list (checking for max containers size)
        # check if picking this container up will exceed max burden

        return True

    def at_object_receive(self, moved_object, source_location, **kwargs):

        print("at_object_receive")

        pass
        # Validate that an object can be received here

        # print(moved_object)
        # Check all packs for available space, move item to first pack with available space (starting with main backpack)

        # if moved_object.is_typeclass(Container):
        #     print("Container!")
        #     self.inventory.packs.append(moved_object)
        # else:
        #     moved_object.move_to(self.inventory.backpack, quiet=True)

        # self.inventory._save()
        # return self.equipment.validate_slot_usage(moved_object)

    def at_object_leave(self, moved_object, source_location, **kwargs):

        pass
        # print("def: at_object_leave")
        # print(ItemType.Container)
        # print(moved_object.db.item_type_int)

        # if moved_object.db.item_type_int == ItemType.Container:
        #     print("yes is pack")
        #     self.inventory.packs.remove(moved_object)
        # # else:
        # #     moved_object.move_to(self.inventory.backpack, quiet=True)

        # self.inventory._save()
        # pass

        # self.inventory._save()

        # Validate that an object can be received here
        # pass
        # return self.equipment.validate_slot_usage(moved_object)
        # self[vital] = new_value

        # Validate that an object can be received here

        # return self.equipment.validate_slot_usage(moved_object)

    def attack(self, target):

        print('Attacking a target with currently wieled weapon (melee or ranged)')

        if not target or not target.is_alive:
            print('No target to attack')
            self.cancel_attack()
            # self.at_post_attack()
            return

        if target.location != self.location:
            print("Target is out of range (moved to another room)")
            self.cancel_attack()
            # self.at_post_attack()
            return

        self.combat_target = target

        # Point of no return, attack will happen
        self.attacking = True

        if self.attacking:

            print("Attacking target:")
            print(self.combat_target)

            # target = self.attributes.get(WeeniePropIID.CurrentCombatTarget.value, default=None)

            damage_amount = round(random.uniform(1, 5))

            self.damage_target(target, damage_amount)

            # prompt = f"|x<|n|r{self.combat_target.vitals.health.current}|n|R/{self.combat_target.vitals.health.max}h|n |y{self.combat_target.vitals.stamina.current}|n|Y/{self.combat_target.vitals.stamina.max}s|n |b{self.combat_target.vitals.mana.current}|n|B/{self.combat_target.vitals.mana.max}m|n|x>|n"

            # self.combat_target.msg(prompt=prompt)

            attack_speed = 5

            if self.combat_target and self.combat_target.is_alive:
                self.combat_timer = delay(
                    attack_speed, self.attack, target, persistent=False)
            else:
                self.at_post_attack()

            # if not self.combat_target.is_attacking:
            #     self.combat_target.start_attack_target(self)

            # PERFORM ATTACK HERE

            # Calculate attack speed to set delay

            # Calculate damage from a bunch of factors (monster weapon, attributes)

            # Queue next attack if target still alive and combat hasn't been cancelled

        # npc_combat_script = self.scripts.get('npc_combat')
        # self.scripts.start('npc_combat')

        # print(npc_combat_script)
        # npc_combat_script.start()

        # self.attributes.set(
        #     WeeniePropIID.CurrentCombatTarget.value,
        #     category="properties",
        #     default=None
        # )

    def at_post_attack(self):

        # Get total attack speed to pass to delay timer

        print('attack sequence is complete')
        self.attacking = False
        self.combat_target = None
        self.combat_timer = None
        return

        # attack ended

    def cancel_attack(self):

        print("Stopping attack")
        # self.scripts.stop('npc_combat')
        # self.attributes.add(WeeniePropIID.CurrentCombatTarget.value, None)

        self.attacking = False
        self.combat_target = None
        self.repeat_attack = False
        self.combat_timer = None

        if self.attacking:
            self.attack_cancelled = True
            # else if (AttackTarget != null)
            #     OnAttackDone();

    def damage_target(self, target, damage_amount):

        target.take_damage(self, damage_amount)

        if self.is_player:
            self.msg(f"|rYou scratch {self.combat_target.name} for {damage_amount} points of slashing damage!|n")

    def take_damage(self, source, damage_amount):

        current_health = self.vitals.health.current

        print('HEALTH STATS')
        print(current_health)
        print(current_health - damage_amount)

        if (current_health - damage_amount) <= 0:
            # Kill creature/player
            self.die(source)
        else:
            new_health = current_health - damage_amount
            self.vitals.update_vital("health", new_health)
            if self.is_player:
                self.msg(f"|R{source.name} scratches you for {damage_amount} points of slashing damage!|n")
                # send updated prompt?

                # prompt = f"|x<|n|r{self.vitals.health.current}|n|R/{self.vitals.health.max}h|n |y{self.vitals.stamina.current}|n|Y/{self.vitals.stamina.max}s|n |b{self.vitals.mana.current}|n|B/{self.vitals.mana.max}m|n|x>|n"

                # self.msg(prompt=prompt)
    
    def die(self, source):

        # self.dead = True

        self.vitals.update_vital("health", 0)

        self.cancel_attack()

        if source.is_player:
            source.msg(f"You killed {self.name}!")


        if self.is_player:

            if source == self:
                self.msg(f"|GAck! You killed yourself!|n")
            else:
                self.msg(f"|GYour seared corpse smolders before {source.name}!|n")
            

            # Drop a corpse in current location
            # Set new vitals
            # Return to the lifestone


            self.location = self.home
            # self.dead = False
        else:
            print("Not a player, so killing!")
            # self.create_corpse()
            self.delete()

            # Handle monster death

            # Drop corpse in current location with loot

            # Delete current object

    def at_death(self):

        # Set new vitals
        #

        pass

    def create_corpse(self):
        
        print('Creating corpse')
        corpse_name = f"Corpse of {self.name}"

        corpse_proto = {
            "prototype_parent": "wcid_21",
            "key": corpse_name,
            "location": self.location
        }

        print(corpse_proto)

        spawner.spawn(corpse_proto)
        pass
