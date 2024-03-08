ATTRIBUTE_MIN_VALUE = 10

from enums import WeeniePropInt, WeeniePropAttribute

class CreatureAttribute:

    def __init__(self, obj, enum, data):
        self.obj = obj
        self.emum = enum
        self.data = data

    @property
    def base(self):
        return self.data["init_Level"] + self.data["level_From_C_P"]

class AttributesHandler:
    """
    Creature attribute handler

    """

    def _load(self):

        strength = self.obj.attributes.get(
            WeeniePropAttribute.Strength.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        endurance = self.obj.attributes.get(
            WeeniePropAttribute.Endurance.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        coordination = self.obj.attributes.get(
            WeeniePropAttribute.Coordination.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        quickness = self.obj.attributes.get(
            WeeniePropAttribute.Quickness.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        focus = self.obj.attributes.get(
            WeeniePropAttribute.Focus.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")
        
        willpower = self.obj.attributes.get(
            WeeniePropAttribute.Willpower.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        self.strength = CreatureAttribute(self.obj, WeeniePropAttribute.Strength, strength)
        self.endurance = CreatureAttribute(self.obj, WeeniePropAttribute.Endurance, endurance)
        self.coordination = CreatureAttribute(self.obj, WeeniePropAttribute.Coordination, coordination)
        self.quickness = CreatureAttribute(self.obj, WeeniePropAttribute.Quickness, quickness)
        self.focus = CreatureAttribute(self.obj, WeeniePropAttribute.Focus, focus)
        self.willpower = CreatureAttribute(self.obj, WeeniePropAttribute.Willpower, willpower)
        
    def _save(self):

        self.obj.attributes.add(
            WeeniePropAttribute.Strength.value, self.strength.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute.Endurance.value, self.endurance.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute.Coordination.value, self.coordination.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute.Quickness.value, self.quickness.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute.Focus.value, self.focus.data, category="properties")
        self.obj.attributes.add(
            WeeniePropAttribute.Willpower.value, self.willpower.data, category="properties")

        self._load()  # important

    def __init__(self, obj):

        print("AttributesHandler __init__")
        self.obj = obj
        self._load()
