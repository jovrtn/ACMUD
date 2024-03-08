
from typeclasses.creatures import Creature


class Monster(Creature):
    """
    This is a base class for monsters.
    """
    name_color = "|420"

    def at_heartbeat(self):
        
        # print('Monster heartbeat')

        # print(self.combat_target)
        if self.combat_target:
            # print('Combat target exists?')
            self.attack(self.combat_target)

    # check if vitals are below 0 first?
        self.vitals.regen()

        # Improve this to check if there are any enchantments that have expirations set first?
        if self.enchantments.all:
            self.enchantments.check_expired()

    # check expired buffs