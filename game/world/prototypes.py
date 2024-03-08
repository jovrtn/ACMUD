"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

For example, you might have a Sword typeclass that implements everything a
Sword would need to do. The only difference between different individual Swords
would be their key, description and some Attributes. The Prototype system
allows to create a range of such Swords with only minor variations. Prototypes
can also inherit and combine together to form entire hierarchies (such as
giving all Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a hierarchy of
typeclasses instead.

A prototype can either be a dictionary placed into a global variable in a
python module (a 'module-prototype') or stored in the database as a dict on a
special Script (a db-prototype). The former can be created just by adding dicts
to modules Evennia looks at for prototypes, the latter is easiest created
in-game via the `olc` command/menu.

Prototypes are read and used to create new objects with the `spawn` command
or directly via `evennia.spawn` or the full path `evennia.prototypes.spawner.spawn`.

A prototype dictionary have the following keywords:

Possible keywords are:
- `prototype_key` - the name of the prototype. This is required for db-prototypes,
  for module-prototypes, the global variable name of the dict is used instead
- `prototype_parent` - string pointing to parent prototype if any. Prototype inherits
  in a similar way as classes, with children overriding values in their parents.
- `key` - string, the main object identifier.
- `typeclass` - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
- `location` - this should be a valid object or #dbref.
- `home` - valid object or #dbref.
- `destination` - only valid for exits (object or #dbref).
- `permissions` - string or list of permission strings.
- `locks` - a lock-string to use for the spawned object.
- `aliases` - string or list of strings.
- `attrs` - Attributes, expressed as a list of tuples on the form `(attrname, value)`,
  `(attrname, value, category)`, or `(attrname, value, category, locks)`. If using one
   of the shorter forms, defaults are used for the rest.
- `tags` - Tags, as a list of tuples `(tag,)`, `(tag, category)` or `(tag, category, data)`.
-  Any other keywords are interpreted as Attributes with no category or lock.
   These will internally be added to `attrs` (equivalent to `(attrname, value)`.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.

"""

from enums import WeeniePropInt, WeeniePropBool, ItemType, BondedStatus, EquipMask, WeeniePropAttribute2nd

# ACE Starter Gear
# https://raw.githubusercontent.com/ACEmulator/ACE/a7205b3104b922d3c1c95b3ecec8d82bebc39299/Source/ACE.Server/starterGear.json

# SACK = {
#     "typeclass": "typeclasses.containers.Container",
#     "key": "Sack",
#     "item_type": ItemType.Container,
#     "value": 65,
#     "encumb_val": 16,
#     "items_capacity": 24
# }

# TACHI = {
#     "typeclass": "typeclasses.melee_weapons.MeleeWeapon",
#     "key": "Tachi",
#     "item_type": ItemType.MeleeWeapon,
#     "value": 100,
#     "encumb_val": 100

# }

# BACKPACK = {
#     "typeclass": "typeclasses.containers.Container",
#     "prototype_key": "mainpack",
#     "key": "Backpack",
#     "attrs": [
#         (WeeniePropInt.ItemType.value, ItemType.Container.value, "properties"),
#         (WeeniePropInt.EncumbVal.value, 0, "properties"),
#         (WeeniePropInt.ItemsCapacity.value, 102, "properties"),
#         (WeeniePropInt.Value.value, 0, "properties"),
#         (WeeniePropInt.Bonded.value, BondedStatus.Sticky.value, "properties")
#     ]
# }

SACK = {
    "typeclass": "typeclasses.containers.Container",
    "key": "Sack",
    "prototype_key": "wcid_166",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Container.value, "properties"),
        (WeeniePropInt.EncumbVal.value, 16, "properties"),
        (WeeniePropInt.ItemsCapacity.value, 24, "properties"),
        (WeeniePropInt.Value.value, 65, "properties"),
    ]
}


FOCI_WAR = {
    "typeclass": "typeclasses.containers.Container",
    "key": "Foci of Strife",
    "prototype_key": "wcid_15271",
    "attrs": [
        ("desc", "A foci used to cast spells from the School of the Arm."),
        (WeeniePropInt.ItemType.value, ItemType.Container.value, "properties"),
        (WeeniePropInt.EncumbVal.value, 400, "properties"),
        (WeeniePropInt.ItemsCapacity.value, 0, "properties"),
        (WeeniePropInt.Value.value, 500, "properties"),
        (WeeniePropInt.Bonded.value, BondedStatus.Bonded.value, "properties")
    ]
}


CALLING_STONE = {
    "typeclass": "typeclasses.gems.Gem",
    "prototype_key": "wcid_5084",
    "key": "Calling Stone",
    "attrs": [
        ("desc", "This is a Calling Stone that all newcomers arrive with. It is a plain, lightweight gem. Give this item to the Society Greeter."),
        (WeeniePropInt.ItemType.value, ItemType.Gem.value, "properties"),
        (WeeniePropInt.EncumbVal.value, 5, "properties"),
        (WeeniePropInt.Value.value, 0, "properties"),
    ]
}

LIFESTONE = {
    "typeclass": "typeclasses.lifestones.Lifestone",
    "prototype_key": "wcid_509",
    "key": "Lifestone",
    "attrs": [
        ("desc", "This is a Calling Stone that all newcomers arrive with. It is a plain, lightweight gem. Give this item to the Society Greeter."),
        (WeeniePropInt.ItemType.value, ItemType.LifeStone.value, "properties"),
        (WeeniePropInt.EncumbVal.value, 5, "properties"),
        (WeeniePropInt.Value.value, 0, "properties"),
        (WeeniePropBool.Stuck.value, True, "properties")
    ]
}

PORTAL_GATEWAY = {
    "typeclass": "typeclasses.portals.Portal",
    "prototype_key": "wcid_1955",
    "key": "Gateway",
    "locks": "get:false()",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Portal.value, "properties"),
    ]
}

HOLT_MEETING_HALL_PORTAL = {
    "typeclass": "typeclasses.portals.Portal",
    "prototype_key": "wcid_6096",
    "key": "Holtburg Meeting Hall Portal",
    "locks": "get:false()",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Portal.value, "properties"),
        (WeeniePropBool.Stuck.value, True, "properties")
    ]
}


NPC_ALCOTT = {
    "typeclass": "typeclasses.npcs.NPC",
    "prototype_key": "wcid_44895",
    "key": "Alcott",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Creature.value, "properties"),
        (WeeniePropBool.Stuck.value, True, "properties")
    ]
}

NPC_RAND = {
    "typeclass": "typeclasses.npcs.NPC",
    "prototype_key": "wcid_39983",
    "key": "Rand, Game Hunter",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Creature.value, "properties"),
        (WeeniePropBool.Stuck.value, True, "properties")
    ]
}

TRAINING_DAGGER  = {
    "typeclass": "typeclasses.melee_weapons.MeleeWeapon",
    "prototype_key": "wcid_45538",
    "key": "Training Dagger",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.MeleeWeapon.value, "properties"),
        (WeeniePropInt.Locations.value, EquipMask.MeleeWeapon.value, "properties")
    ]
}

TRAINING_SPADONE = {
    "typeclass": "typeclasses.melee_weapons.MeleeWeapon",
    "prototype_key": "wcid_41512",
    "key": "Training Spadone",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.MeleeWeapon.value, "properties"),
        (WeeniePropInt.Locations.value, EquipMask.TwoHanded.value, "properties")
    ]
}

MATTEKAR_COAT = {
    "typeclass": "typeclasses.armors.Armor",
    "prototype_key": "wcid_4231",
    "key": "Mattekar Hide Coat",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Armor.value, "properties"),
        (WeeniePropInt.Locations.value, 7680, "properties"),
        (WeeniePropInt.EncumbVal.value, 810, "properties"),
        (WeeniePropInt.Value.value, 800, "properties"),
    ]
}

BUCKLER = {
    "typeclass": "typeclasses.armors.Armor",
    "prototype_key": "wcid_44",
    "key": "Buckler",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Armor.value, "properties"),
        (WeeniePropInt.Locations.value, 2097152, "properties"),
        (WeeniePropInt.EncumbVal.value, 200, "properties"),
        (WeeniePropInt.Value.value, 200, "properties"),
    ]
}

ARROW = {
    "typeclass": "typeclasses.ammunitions.Ammunition",
    "prototype_key": "wcid_300",
    "key": "Arrow",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.MissileWeapon.value, "properties"),
        (WeeniePropInt.Locations.value, 8388608, "properties"),
        (WeeniePropInt.EncumbVal.value, 5, "properties"),
        (WeeniePropInt.Value.value, 1, "properties"),
    ]
}

BREASTPLATE = {
    "typeclass": "typeclasses.armors.Armor",
    "prototype_key": "wcid_40",
    "key": "Platemail Breastplate",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Armor.value, "properties"),
        (WeeniePropInt.Locations.value, 512, "properties"),
        (WeeniePropInt.EncumbVal.value, 800, "properties"),
        (WeeniePropInt.Value.value, 1000, "properties"),
    ]
}



DRUDGE = {
    "typeclass": "typeclasses.monsters.Monster",
    "prototype_key": "wcid_7",
    "key": "Drudge Skulker",
    "attrs": [
        (WeeniePropInt.ItemType.value, ItemType.Creature.value, "properties"),
        (WeeniePropBool.Attackable.value, True, "properties"),
        (WeeniePropBool.Stuck.value, True, "properties"),
        (WeeniePropAttribute2nd.MaxHealth.value, {"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 50}, "properties")
    ]
}


DRUDGE_GENERATOR = {
    "typeclass": "typeclasses.generators.Generator",
    "prototype_key": "wcid_381",
    "key": "Drudge Generator",
    "attrs": [
        (WeeniePropBool.Visibility.value, False, "properties"),
        (WeeniePropBool.Stuck.value, True, "properties")
    ]
}

CORPSE = {
    "typeclass": "typeclasses.corpses.Corpse",
    "prototype_key": "wcid_21",
    "key": "Corpse",
    "attrs": [
        (WeeniePropBool.Stuck.value, True, "properties")
    ]
}



# # TEST_OBJ = {
# #     "typeclass": "typeclasses.containers.Contar",
# #     "key": "Test Container",
#     "attrs": [
#         # ("desc", "This is a Calling Stone that all newcomers arrive with. It is a plain, lightweight gem. Give this item to the Society Greeter."),
#         ("item_type", ItemType.Gem.value),
#         ("value", 0),
#        # ("encumb_val", 5)
#     ]

# # }


# example of module-based prototypes using
# the variable name as `prototype_key` and
# simple Attributes

# from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"],
# "tags": = [("greenskin", "monster"), ("humanoid", "monster")]
# }
#
# GOBLIN_WIZARD = {
# "prototype_parent": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype_parent": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
# }
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
# }
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype_parent" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
# }
