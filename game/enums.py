from enum import Enum, IntFlag


class WeeniePropInt(Enum):
    ItemType = "item_type_int"
    CreatureType = "creature_type_int"
    EncumbVal = "encumb_val_int"
    ItemsCapacity = "items_capacity_int"
    ContainersCapacity = "containers_capacity_int"
    Locations = "locations_int"
    CurrentWieldedLocation = "current_wielded_location_int"
    TotalExperience = "total_experience_int"
    TotalSkillCredits = "total_skill_credits_int"
    AvailableSkillCredits = "available_skill_credits_int"
    ArmorLevel = "armor_level_int"
    Bonded = "bonded_int"
    MonarchsRank = "monarchs_rank_int"
    ResistMagic = "resist_magic_int"
    Value = "value_int"
    Enlightenment = "enlightenment_int"


WEENIE_PROPS_INT_REVERSE_MAP = {
    1: WeeniePropInt.ItemType,
    2: WeeniePropInt.CreatureType,

    5: WeeniePropInt.EncumbVal,
    6: WeeniePropInt.ItemsCapacity,
    7: WeeniePropInt.ContainersCapacity,
    9: WeeniePropInt.Locations,
    10: WeeniePropInt.CurrentWieldedLocation,

    19: WeeniePropInt.Value,
    21: WeeniePropInt.TotalExperience,
    23: WeeniePropInt.TotalSkillCredits,
    24: WeeniePropInt.AvailableSkillCredits,

    28: WeeniePropInt.ArmorLevel,

    33: WeeniePropInt.Bonded,
    34: WeeniePropInt.MonarchsRank,

    36: WeeniePropInt.ResistMagic,


    390: WeeniePropInt.Enlightenment
}


class WeeniePropBool(Enum):
    Inscribable = "inscribable_bool"
    Stuck = "stuck_bool"
    Attackable = "attackable_bool"
    Visibility = "visibility_bool"


WEENIE_PROPS_BOOL_REVERSE_MAP = {
    1: WeeniePropBool.Stuck,

    18: WeeniePropBool.Visibility,
    19: WeeniePropBool.Attackable,

    22: WeeniePropBool.Inscribable,
}


class WeeniePropString(Enum):
    Title = "title_string"
    Inscription = "inscription_string"
    ScribeName = "scribe_name_string"


WEENIE_PROPS_STRING_REVERSE_MAP = {

    2: WeeniePropString.Title,

    7: WeeniePropString.Inscription,
    8: WeeniePropString.ScribeName
}


class WeeniePropPosition(Enum):
    Destination = "destination_position"


WEENIE_PROPS_STRING_REVERSE_MAP = {
    2: WeeniePropPosition.Destination,
}


class WeeniePropIID(Enum):
    Generator = "generator_iid"
    CurrentCombatTarget = "current_combat_target_iid"


WEENIE_PROPS_IID_REVERSE_MAP = {
    6: WeeniePropIID.Generator,
    8: WeeniePropIID.CurrentCombatTarget,
}


class WeeniePropAttribute(Enum):
    Strength = "strength_attribute"
    Endurance = "endurance_attribute"
    Coordination = "coordination_attribute"
    Quickness = "quickness_attribute"
    Focus = "focus_attribute"
    Willpower = "self_attribute"


WEENIE_PROPS_ATTRIBUTE_REVERSE_MAP = {
    1: WeeniePropAttribute.Strength,
    2: WeeniePropAttribute.Endurance,
    3: WeeniePropAttribute.Coordination,
    4: WeeniePropAttribute.Quickness,
    5: WeeniePropAttribute.Focus,
    6: WeeniePropAttribute.Willpower
}



class WeeniePropAttribute2nd(Enum):
    MaxHealth = "max_health_attribute_2nd"
    MaxStamina = "max_stamina_attribute_2nd"
    MaxMana = "max_mana_attribute_2nd"


WEENIE_PROPS_ATTRIBUTE_2ND_REVERSE_MAP = {
    1: WeeniePropAttribute2nd.MaxHealth,
    3: WeeniePropAttribute2nd.MaxStamina,
    5: WeeniePropAttribute2nd.MaxMana
}


# TestItemType = Enum("TestItemType", ["Gem"], start=0)

# class TestItemType(Enum):
#     Gem = "gem"

# class WeenieType(Enum):
#     Undef = 0
#     Generic = auto()
#     Clothing = auto()
#     MissileLauncher = auto()
#     Missile = auto()
#     Ammunition = auto()
#     MeleeWeapon = auto()
#     Portal = auto()
#     Book = auto()
#     Coin = auto()
#     Creature = auto()
#     Admin = auto()
#     Vendor = auto()
#     HotSpot = auto()
#     Corpse = auto()
#     Cow = auto()
#     AI = auto()
#     Machine = auto()
#     Food = auto()
#     Door = auto()
#     Chest = auto()
#     Container = auto()
#     Key = auto()
#     Lockpick = auto()
#     PressurePlate = auto()
#     LifeStone = auto()
#     Switch = auto()
#     PKModifier = auto()
#     Healer = auto()
#     LightSource = auto()
#     Allegiance = auto()
#     UNKNOWN__GUESSEDNAME32 = auto()  # NOTE: Missing 1
#     SpellComponent = auto()
#     ProjectileSpell = auto()
#     Scroll = auto()
#     Caster = auto()
#     Channel = auto()
#     ManaStone = auto()
#     Gem = auto()
#     AdvocateFane = auto()
#     AdvocateItem = auto()
#     Sentinel = auto()
#     GSpellEconomy = auto()
#     LSpellEconomy = auto()
#     CraftTool = auto()
#     LScoreKeeper = auto()
#     GScoreKeeper = auto()
#     GScoreGatherer = auto()
#     ScoreBook = auto()
#     EventCoordinator = auto()
#     Entity = auto()
#     Stackable = auto()
#     HUD = auto()
#     House = auto()
#     Deed = auto()
#     SlumLord = auto()
#     Hook = auto()
#     Storage = auto()
#     BootSpot = auto()
#     HousePortal = auto()
#     Game = auto()
#     GamePiece = auto()
#     SkillAlterationDevice = auto()
#     AttributeTransferDevice = auto()
#     Hooker = auto()
#     AllegianceBindstone = auto()
#     InGameStatKeeper = auto()
#     AugmentationDevice = auto()
#     SocialManager = auto()
#     Pet = auto()
#     PetDevice = auto()
#     CombatPet = auto()



class ItemType(IntFlag):
    NoneValue = 0x00000000
    MeleeWeapon = 0x00000001
    Armor = 0x00000002
    Clothing = 0x00000004
    Jewelry = 0x00000008
    Creature = 0x00000010
    Food = 0x00000020
    Money = 0x00000040
    Misc = 0x00000080
    MissileWeapon = 0x00000100
    Container = 0x00000200
    Useless = 0x00000400
    Gem = 0x00000800
    SpellComponents = 0x00001000
    Writable = 0x00002000
    Key = 0x00004000
    Caster = 0x00008000
    Portal = 0x00010000
    Lockable = 0x00020000
    PromissoryNote = 0x00040000
    ManaStone = 0x00080000
    Service = 0x00100000
    MagicWieldable = 0x00200000
    CraftCookingBase = 0x00400000
    CraftAlchemyBase = 0x00800000
    CraftFletchingBase = 0x02000000
    CraftAlchemyIntermediate = 0x04000000
    CraftFletchingIntermediate = 0x08000000
    LifeStone = 0x10000000
    TinkeringTool = 0x20000000
    TinkeringMaterial = 0x40000000
    Gameboard = 0x80000000

    PortalMagicTarget = Portal | LifeStone
    LockableMagicTarget = Misc | Container
    Vestements = Armor | Clothing
    Weapon = MeleeWeapon | MissileWeapon
    WeaponOrCaster = MeleeWeapon | MissileWeapon | Caster
    Item = MeleeWeapon | Armor | Clothing | Jewelry | Food | Money | Misc | MissileWeapon | Container | Gem | SpellComponents | Writable | Key | Caster | Portal | PromissoryNote | ManaStone | MagicWieldable
    RedirectableItemEnchantmentTarget = MeleeWeapon | Armor | Clothing | MissileWeapon | Caster
    ItemEnchantableTarget = MeleeWeapon | Armor | Clothing | Jewelry | Misc | MissileWeapon | Container | Gem | Caster | ManaStone
    VendorShopKeep = MeleeWeapon | Armor | Clothing | Food | Misc | MissileWeapon | Container | Useless | Writable | Key | PromissoryNote | CraftFletchingIntermediate | TinkeringMaterial
    VendorGrocer = Food | Container | Writable | Key | PromissoryNote | CraftCookingBase


class BondedStatus(Enum):
    Destroy = -2
    Slippery = -1
    Normal = 0
    Bonded = 1
    Sticky = 2


class AttunedStatus(Enum):
    Normal = 0
    Attuned = 1

class EquipMask(IntFlag):
    NoneValue = 0x00000000
    HeadWear = 0x00000001
    ChestWear = 0x00000002
    AbdomenWear = 0x00000004
    UpperArmWear = 0x00000008
    LowerArmWear = 0x00000010
    HandWear = 0x00000020
    UpperLegWear = 0x00000040
    LowerLegWear = 0x00000080
    FootWear = 0x00000100
    ChestArmor = 0x00000200
    AbdomenArmor = 0x00000400
    UpperArmArmor = 0x00000800
    LowerArmArmor = 0x00001000
    UpperLegArmor = 0x00002000
    LowerLegArmor = 0x00004000
    NeckWear = 0x00008000
    WristWearLeft = 0x00010000
    WristWearRight = 0x00020000
    FingerWearLeft = 0x00040000
    FingerWearRight = 0x00080000
    MeleeWeapon = 0x00100000
    Shield = 0x00200000
    MissileWeapon = 0x00400000
    MissileAmmo = 0x00800000
    Held = 0x01000000
    TwoHanded = 0x02000000
    TrinketOne = 0x04000000
    Cloak = 0x08000000
    SigilOne = 0x10000000
    SigilTwo = 0x20000000
    SigilThree = 0x40000000
    Clothing = 0x80000000 | HeadWear | ChestWear | AbdomenWear | UpperArmWear | LowerArmWear | HandWear | UpperLegWear | LowerLegWear | FootWear
    Armor = ChestArmor | AbdomenArmor | UpperArmArmor | LowerArmArmor | UpperLegArmor | LowerLegArmor | FootWear
    ArmorExclusive = ChestArmor | AbdomenArmor | UpperArmArmor | LowerArmArmor | UpperLegArmor | LowerLegArmor
    Extremity = HeadWear | HandWear | FootWear
    Jewelry = NeckWear | WristWearLeft | WristWearRight | FingerWearLeft | FingerWearRight | TrinketOne | Cloak | SigilOne | SigilTwo | SigilThree
    WristWear = WristWearLeft | WristWearRight
    FingerWear = FingerWearLeft | FingerWearRight
    Sigil = SigilOne | SigilTwo | SigilThree
    ReadySlot = Held | TwoHanded | TrinketOne | Cloak | SigilOne | SigilTwo
    Weapon = SigilTwo | TrinketOne | Held
    WeaponReadySlot = SigilOne | SigilTwo | TrinketOne | Held
    Selectable = MeleeWeapon | Shield | MissileWeapon | Held | TwoHanded
    SelectablePlusAmmo = Selectable | MissileAmmo
    All = 0x7FFFFFFF
    CanGoInReadySlot = 0x7FFFFFFF

class EquipSlot(Enum):
    Head = "head"
    Chest = "chest"
    Abdomen = "abdomen"
    UpperArm = "upper_arm"
    LowerArm = "lower_arm"
    Hands = "hands"
    Feet = "feet"
    UpperLeg = "upper_leg"
    LowerLeg = "lower_leg"
    Neck = "neck"
    WristLeft = "wrist_left"
    WristRight = "wrist_right"
    FingerLeft = "finger_left"
    FingerRight = "finger_right"
    MainHand = "main_hand"
    OffHand = "off_hand"
    Trinket = "trinket"
    Ammunition = "ammunition"
    SigilOne = "sigil_one"
    SigilTwo = "sigil_two"
    SigilThree = "sigil_three"
    Shirt = "shirt"
    Pants = "pants"
    Cloak = "cloak"

class EquipSlotMask(IntFlag):
    Head = EquipMask.HeadWear
    Chest = EquipMask.ChestArmor
    Abdomen = EquipMask.AbdomenArmor
    UpperArm = EquipMask.UpperArmArmor
    LowerArm = EquipMask.LowerArmArmor
    Hands = EquipMask.HandWear
    Feet = EquipMask.FootWear
    UpperLeg = EquipMask.UpperLegArmor
    LowerLeg = EquipMask.LowerLegArmor
    Neck = EquipMask.NeckWear
    WristLeft = EquipMask.WristWearLeft
    WristRight = EquipMask.WristWearRight
    FingerLeft = EquipMask.FingerWearLeft
    FingerRight = EquipMask.FingerWearRight
    MainHand = EquipMask.TwoHanded | EquipMask.MeleeWeapon | EquipMask.Held | EquipMask.MissileWeapon
    OffHand = EquipMask.Shield
    Trinket = EquipMask.TrinketOne
    Ammunition = EquipMask.MissileAmmo
    SigilOne = EquipMask.SigilOne
    SigilTwo = EquipMask.SigilTwo
    SigilThree = EquipMask.SigilThree
    Shirt = EquipMask.ChestWear | EquipMask.AbdomenWear | EquipMask.UpperArmWear | EquipMask.LowerArmWear | EquipMask.UpperLegWear | EquipMask.LowerLegWear | EquipMask.FootWear
    Pants = EquipMask.UpperLegWear | EquipMask.LowerLegWear
    Cloak = EquipMask.Cloak

# class EquipmentSlot(IntFlag):
#     ChestArmor = EquipMask.ChestArmor
#     AbdomenArmor = EquipMask.AbdomenArmor
#     UpperArmArmor = EquipMask.UpperArmArmor
#     LowerArmArmor = EquipMask.LowerArmArmor
#     UpperLegArmor = EquipMask.UpperLegArmor
#     LowerLegArmor = EquipMask.LowerLegArmor
#     NeckWear = EquipMask.NeckWear
#     WristWearLeft = EquipMask.WristWearLeft
#     WristWearRight = EquipMask.WristWearRight
#     FingerWearLeft = EquipMask.FingerWearLeft
#     FingerWearRight = EquipMask.FingerWearRight
#     MeleeWeapon = EquipMask.MeleeWeapon
#     Shield = EquipMask.Shield
#     MissileWeapon = EquipMask.MissileWeapon
#     MissileAmmo = EquipMask.MissileAmmo
#     TrinketOne = EquipMask.TrinketOne
#     Cloak = EquipMask.Cloak
#     SigilOne = EquipMask.SigilOne
#     SigilTwo = EquipMask.SigilTwo
#     SigilThree = EquipMask.SigilThree
#     UpperWear = EquipMask.ChestWear
#     LowerWear = EquipMask.UpperLegWear


class CreaturePose(Enum):
    Standing = "standing"
    Crouching = "crouching"
    Sitting = "sitting"
    Sleeping = "sleeping"
