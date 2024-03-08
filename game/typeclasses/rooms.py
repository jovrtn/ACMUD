"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from typeclasses.exits import Door

from typeclasses.npcs import NPC
from typeclasses.characters import Character
from typeclasses.monsters import Monster

from evennia.utils.utils import inherits_from
from .objects import ObjectParent
from evennia.utils.utils import (
    class_from_module,
    dbref,
    is_iter,
    iter_to_str,
    lazy_property,
    make_iter,
    to_str,
    variable_from_module,
)

class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    appearance_template = """
{header}
|w|u{name}|n
{exits}
|x{desc}|n
{things}{characters}
{footer}
        """

    def get_display_exits(self, looker, **kwargs):
        """
        Get the 'exits' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The exits display data.

        """

        print(self.exits)

        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        exits = _filter_visible(self.contents_get(content_type="exit"))

        # for exi in self.exits:
        #     locked = exi.locks.check(looker, "traverse")
        #     print(locked)


        exit_names = []

        for exi in exits:
            label = exi.name
            if inherits_from(exi, Door):
                access = exi.locks.check(looker, "traverse")

                # access = exi.access(looker)

                print(access)

                open_label = ""
                if access:
                    open_label = "open"
                else:
                    open_label = "closed"

             
                # if locked: label
                label = f"{label}({open_label})"
            exit_names.append(label)

        # exit_names = iter_to_str(exi.get_display_name(looker, **kwargs) for exi in exits)

        return "[Exits: {}]".format(", ".join(exit_names)) if exit_names else ""

    def get_display_things(self, looker, **kwargs):
        """
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The things display data.

        """

        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        excluded_typeclasses = [NPC, Monster]
        objects = self.contents_get(content_type="object");
        # sort and handle same-named things

        things = [x for x in objects if not any(x.is_typeclass(tc) for tc in excluded_typeclasses)]

        things_visible = _filter_visible(things)

        # grouped_things = defaultdict(list)
        # for thing in things:
        #     grouped_things[thing.get_display_name(looker, **kwargs)].append(thing)

        # thing_names = []
        # for thingname, thinglist in sorted(grouped_things.items()):
        #     nthings = len(thinglist)
        #     thing = thinglist[0]
        #     singular, plural = thing.get_numbered_name(nthings, looker, key=thingname)
        #     thing_names.append(singular if nthings == 1 else plural)
        # thing_names = iter_to_str(thing_names)

        thing_names = []
        
        for thing in things:
            thing_names.append(f"    {thing.get_display_name(looker, **kwargs)}")

    
        return "|x{}|n".format("\n".join(thing_names)) if thing_names else ""

    def get_display_characters(self, looker, **kwargs):
        """
        Get the 'characters' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The character display data.

        """

        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        creature_typeclasses = [NPC, Character, Monster]
        creatures = [x for x in self.contents if any(x.is_typeclass(tc) for tc in creature_typeclasses)]
        creatures_visible = _filter_visible(creatures)
        creature_names = []

        for creature in creatures_visible:
            name = creature.get_display_name(looker, **kwargs)
            title = creature.attributes.get("title_string")
            if title:
                name = f"{name}|x, {title}|n"
            name = f"{name}|x is here.|n"
            creature_names.append(name)
        
        return "\n{}".format("\n".join(creature_names)) if creature_names else ""


    def at_object_receive(self, moved_obj, source_location, move_type='move', **kwargs):

        print("New object in room")
        print(moved_obj)
    
        # If new object is a character

        if moved_obj.is_typeclass('typeclasses.characters.Character'):
            print('is character')
        # Get list of all creatures in the room

    

    pass
