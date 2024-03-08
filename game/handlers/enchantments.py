
from enums import WeeniePropInt, WeeniePropAttribute
import time


class Enchantment:

    def __init__(self, obj, data, duration=0):
        self.obj = obj
        self.data = data
        self.duration = duration

    # @property
    # def base(self):
    #     return self.data["init_Level"] + self.data["level_From_C_P"]


class EnchantmentsHandler:
    """
    Object enchantments handler

    """

    save_attribute = "_enchantments"

    def _load(self):

        self.enchantments = self.obj.attributes.get(
            self.save_attribute,
            category="enchantments",
            default=[])

        # strength = self.obj.attributes.get(
        #     WeeniePropAttribute.Strength.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        # endurance = self.obj.attributes.get(
        #     WeeniePropAttribute.Endurance.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        # coordination = self.obj.attributes.get(
        #     WeeniePropAttribute.Coordination.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        # quickness = self.obj.attributes.get(
        #     WeeniePropAttribute.Quickness.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        # focus = self.obj.attributes.get(
        #     WeeniePropAttribute.Focus.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        # willpower = self.obj.attributes.get(
        #     WeeniePropAttribute.Willpower.value, default={"init_Level": ATTRIBUTE_MIN_VALUE, "level_From_C_P": 0, "c_P_Spent": 0}, category="properties")

        # setattr(self, "strength", CreatureAttribute(self.obj, WeeniePropAttribute.Strength, strength))
        # setattr(self, "endurance", CreatureAttribute(self.obj, WeeniePropAttribute.Endurance, endurance))
        # setattr(self, "coordination", CreatureAttribute(self.obj, WeeniePropAttribute.Coordination, coordination))
        # setattr(self, "quickness", CreatureAttribute(self.obj, WeeniePropAttribute.Quickness, quickness))
        # setattr(self, "focus", CreatureAttribute(self.obj, WeeniePropAttribute.Focus, focus))
        # setattr(self, "willpower", CreatureAttribute(self.obj, WeeniePropAttribute.Willpower, willpower))

    def _save(self):

        self.obj.attributes.add(
            self.save_attribute,
            self.enchantments,
            category="enchantments")

        # strength = self.obj.attributes.add(
        #     WeeniePropAttribute.Strength.value, self.strength.data, category="properties")

        # endurance = self.obj.attributes.add(
        #     WeeniePropAttribute.Endurance.value, self.endurance.data, category="properties")

        # coordination = self.obj.attributes.add(
        #     WeeniePropAttribute.Coordination.value, self.coordination.data, category="properties")

        # quickness = self.obj.attributes.add(
        #     WeeniePropAttribute.Quickness.value, self.quickness.data, category="properties")

        # focus = self.obj.attributes.add(
        #     WeeniePropAttribute.Focus.value, self.focus.data, category="properties")

        # willpower = self.obj.attributes.add(
        #     WeeniePropAttribute.Willpower.value, self.willpower.data, category="properties")

        self._load()  # important

    @property
    def all(self):
        return self.enchantments

    def add(self, source, enchantment, expires_at):

        # Validate, send messages, etc

        # Check if spell with the same ID already exists
        print('Spell added')
        print(enchantment)
        print(expires_at)

        source_name = None
        if source == self.obj:
            source_name = "You"

        self.obj.msg(f"|035{source_name} cast {enchantment['value']['name']}.|n")

        self.enchantments.append(
            {"data": enchantment, "expires_at": expires_at})
        self._save()

    def check_expired(self):
        
        print("Check for expired enchantments")
        now = int(time.time())

        for enchantment in self.enchantments:
            if enchantment["expires_at"] <= now:
                self.obj.msg(f"|035{enchantment['data']['value']['name']} has expired.|n")
                self.enchantments.remove(enchantment)
    


    def __init__(self, obj):

        print("AttributesHandler __init__")
        self.obj = obj
        self._load()
