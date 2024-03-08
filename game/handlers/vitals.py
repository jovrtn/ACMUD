from enums import WeeniePropInt, WeeniePropAttribute2nd

class CreatureVital:
    def __init__(self, obj, enum, data):
        self.obj = obj
        self.enum = enum
        self.data = data
    @property
    def base(self):

        total = self.data["init_Level"] + self.data["level_From_C_P"]
        attrs = 0
        enlightenment = 0
        gear_vitality = 0

        if self.enum == WeeniePropAttribute2nd.MaxHealth:
            attrs = round(self.obj.attribs.endurance.base / 2)
            enlightenment = self.obj.attributes.get(WeeniePropInt.Enlightenment.value, default=0, category="properties") * 2
        elif self.enum == WeeniePropAttribute2nd.MaxStamina:
            attrs = round(self.obj.attribs.endurance.base)
        elif self.enum == WeeniePropAttribute2nd.MaxMana:
            attrs = round(self.obj.attribs.willpower.base)
        
        total = total + attrs + enlightenment + gear_vitality
        
        return total

    @property
    def current(self):
        return self.data["current_Level"]

    @property
    def max(self):
        # Perform min/max innate checks here

        # Calculate multipliers or flat boosts in a specific order here

        # Add in buffs
        return self.base

class VitalsHandler:
    """
    Creature vitals handler

    """

    def _load(self):

        health = self.obj.attributes.get(
            WeeniePropAttribute2nd.MaxHealth.value, default={"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 0}, category="properties")
        stamina = self.obj.attributes.get(
            WeeniePropAttribute2nd.MaxStamina.value, default={"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 0}, category="properties")
        mana = self.obj.attributes.get(
            WeeniePropAttribute2nd.MaxMana.value, default={"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 0}, category="properties")

        self.health = CreatureVital(self.obj, WeeniePropAttribute2nd.MaxHealth, health)
        self.stamina = CreatureVital(self.obj, WeeniePropAttribute2nd.MaxStamina, stamina)
        self.mana = CreatureVital(self.obj, WeeniePropAttribute2nd.MaxMana, mana)

    def _save(self):

        self.obj.attributes.add(
            WeeniePropAttribute2nd.MaxHealth.value, self.health.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute2nd.MaxStamina.value, self.stamina.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute2nd.MaxMana.value, self.mana.data, category="properties")

        self._load()  # important
    
    def regen(self):
        print('Vitals regen')

    def update_vital(self, vital, value):
        print("UPDATE VITAL")
        vital_attr = getattr(self, vital)
        print(vital_attr)
        print(value)
        vital_attr.data["current_Level"] = value
        print(vital_attr.data)
        self._save()

    def __init__(self, obj):

        print("VitalsHandler __init__")
        self.obj = obj
        self._load()