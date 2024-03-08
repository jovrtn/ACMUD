from .objects import ObjectParent


class Weenie(ObjectParent):
    """
    This is a generic weenie
    """

    weenie_type = 'GENERIC'

    burden = AttributeProperty(default=None)
    inscription = AttributeProperty(default=None)
    inscription_author = AttributeProperty(default=None)
    inscribable = AttributeProperty(default=False) 
    properties = AttributeProperty(default=[]) # Attuned, Bonded, etc



class MeleeWeapon(Weenie):
    """
    Base class for all ACMUD melee weapons.

    """

    # Attack types
    # thrust / stab (lowest power)
    # slice (forehand)
    #
    # slash (medium backhand)
    # strike (powerful forehand)

    weenie_type = 'MELEE_WEAPON'
    stackable = False
    
    workmanship = AttributeProperty(default=None)
    material = AttributeProperty(default=None)

    skill = AttributeProperty(default=0)
    mastery = AttributeProperty(default=None)
    damage_types = AttributeProperty(default=0)
    
    damage_low = AttributeProperty(default=0)
    damage_high = AttributeProperty(default=0)
    attack_mod = AttributeProperty(default=0)
    melee_defense_mod = AttributeProperty(default=0)
    speed = AttributeProperty(default=0)

    sellable = AttributeProperty(default=False)

    wield_reqs = AttributeProperty(default=[]) # Skill requirement, player bound, etc
    activation_reqs = AttributeProperty(default=[])

    spellcraft = AttributeProperty(default=0)
    mana = AttributeProperty(default=0)
    mana_cost = AttributeProperty(default=0)
    spells = AttributeProperty(default=[])

    tinkers = AttributeProperty(default=0)
    tinker_name = AttributeProperty(default=None)
    
    augmentations_a = AttributeProperty(default=[])
    augmentations_b = AttributeProperty(default=[])
    augmentations_c = AttributeProperty(default=[])

   
class MagicCaster(Weenie):
    """
    Base class for all ACMUD magic casters.

    """

    # Attack types
    # thrust / stab (lowest power)
    # slice (forehand)
    #
    # slash (medium backhand)
    # strike (powerful forehand)

    weenie_type = 'MAGIC_CASTER'
    stackable = False
    
    workmanship = AttributeProperty(default=None)
    material = AttributeProperty(default=None)
    
    damage_type = AttributeProperty(default=None)
    damage_bonus_monsters = AttributeProperty(default=0)
    damage_bonus_players = AttributeProperty(default=0)

    mana_conv_mod = AttributeProperty(default=0)
    melee_defense_mod = AttributeProperty(default=0)
    magic_defense_mod = AttributeProperty(default=0)

    sellable = AttributeProperty(default=False)

    wield_reqs = AttributeProperty(default=[]) # Skill requirement, player bound, etc
    activation_reqs = AttributeProperty(default=[])

    spellcraft = AttributeProperty(default=0)
    mana = AttributeProperty(default=0)
    mana_cost = AttributeProperty(default=0)
    spells = AttributeProperty(default=[])

    tinkers = AttributeProperty(default=0)
    tinker_name = AttributeProperty(default=None)
    
    augmentations_a = AttributeProperty(default=[])
    augmentations_b = AttributeProperty(default=[])
    augmentations_c = AttributeProperty(default=[])
