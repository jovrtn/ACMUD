"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""


from evennia.objects.objects import DefaultObject
from evennia.typeclasses.attributes import AttributeProperty
from enums import BondedStatus, AttunedStatus, WeeniePropInt, WeeniePropBool, WeeniePropAttribute2nd


class ObjectParent:
    """
    This is a mixin that can be used to override *all* entities inheriting at
    some distance from DefaultObject (Objects, Exits, Characters and Rooms).

    Just add any method that exists on `DefaultObject` to this class. If one
    of the derived classes has itself defined that same hook already, that will
    take precedence.

    """


class Object(ObjectParent, DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_pre_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_post_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_post_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

    """

    combat_target = None
    combat_timer = None

    name_color = "|x"
    weenie_type: int = AttributeProperty(default=None, autocreate=False)

    # Weenie Properties

    # INT

    item_type_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    creature_type_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    encumb_val_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    items_capacity_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    containers_capacity_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")

    locations_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")

    current_wielded_location_int = AttributeProperty(
        default=None, autocreate=False, category="properties")

    creature_type_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")

    total_experience_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    total_skill_credits_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    available_skill_credits_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    armor_level_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    bonded_int: int = AttributeProperty(
        default=AttunedStatus.Normal.value, autocreate=False, category="properties")
    monarchs_rank_int: int = AttributeProperty(
        default=None, autocreate=False, category="properties")
    resist_magic_int: int = AttributeProperty(
        default=0, autocreate=False, category="properties")  # set to 0 or 9999



    enlightenment_int: int = AttributeProperty(
        default=0, autocreate=False, category="properties")

    # RESIST_ITEM_APPRAISAL_INT: int = AttributeProperty(default=0, autocreate=False, category="properties") # set to 0 or 9999
    # RESIST_LOCKPICK_INT: int = AttributeProperty(default=0, autocreate=False, category="properties") # set to 0 or 9999
    # CURRENT_ATTACK_HEIGHT_INT: int = AttributeProperty(default=2, autocreate=False, category="properties")
    # NUM_DEATHS_INT: int = AttributeProperty(default=0, autocreate=False, category="properties")
    # TOLERANCE_INT: int = AttributeProperty(default=0, autocreate=False, category="properties")
    # NUM_CHARACTER_TITLES: int = AttributeProperty(default=0, autocreate=False, category="properties")
    # ATTUNED_INT: int = AttributeProperty(default=AttunedStatus.Normal.value, autocreate=False, category="properties")

    # STRING

    # TITLE_STRING: str = AttributeProperty(default=None, autocreate=False, category="properties")
    # INSCRIPTION_STRING: str = AttributeProperty(default=None, autocreate=False, category="properties")
    # SCRIBE_NAME_STRING: str = AttributeProperty(default=None, autocreate=False, category="properties")

    # BOOL

    stuck_bool: bool = AttributeProperty(
        default=False, autocreate=True, category="properties")
    inscribale_bool: bool = AttributeProperty(
        default=False, autocreate=True, category="properties")

    visibility_bool: bool = AttributeProperty(
        default=True, autocreate=True, category="properties")
    attackable_bool: bool = AttributeProperty(
        default=False, autocreate=True, category="properties")

    # Floats

    health_rate_float = AttributeProperty(
        default=0.5, autocreate=True, category="properties")
    stamina_rate_float = AttributeProperty(
        default=0.5, autocreate=True, category="properties")
    mana_rate_float = AttributeProperty(
        default=0.5, autocreate=True, category="properties")

    # Attributes Primary

    strength_attribute = AttributeProperty(
        default={"init_Level": 10, "level_From_C_P": 0, "c_P_Spent": 0}, autocreate=True, category="properties")
    endurance_attribute = AttributeProperty(
        default={"init_Level": 10, "level_From_C_P": 0, "c_P_Spent": 0}, autocreate=True, category="properties")
    quickness_attribute = AttributeProperty(
        default={"init_Level": 10, "level_From_C_P": 0, "c_P_Spent": 0}, autocreate=True, category="properties")
    coordination_attribute = AttributeProperty(
        default={"init_Level": 10, "level_From_C_P": 0, "c_P_Spent": 0}, autocreate=True, category="properties")
    focus_attribute = AttributeProperty(
        default={"init_Level": 10, "level_From_C_P": 0, "c_P_Spent": 0}, autocreate=True, category="properties")
    self_attribute = AttributeProperty(
        default={"init_Level": 10, "level_From_C_P": 0, "c_P_Spent": 0}, autocreate=True, category="properties")

    # Attributes Secondary (Vitals)

    max_health_attribute_2nd = AttributeProperty(
        default={"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 0}, autocreate=True, category="properties")
    max_stamina_attribute_2nd = AttributeProperty(
        default={"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 0}, autocreate=True, category="properties")
    max_mana_attribute_2nd = AttributeProperty(
        default={"init_Level": 0, "level_From_C_P": 0, "c_P_Spent": 0, "current_Level": 0}, autocreate=True, category="properties")

    # POSITION

    # destination_position = AttributeProperty(default=False, autocreate=False, category="properties")

    dest = AttributeProperty(
        default=None, autocreate=False, category="positions")

    # Instance IDs (IID)
    generator_iid: bool = AttributeProperty(
        default=None, autocreate=True, category="properties")

    current_combat_target_iid: bool = AttributeProperty(
        default=None, autocreate=True, category="properties")

    def at_object_creation(self):
        
        visibility = self.attributes.get(WeeniePropBool.Visibility.value, default=True, category="properties")
        if not visibility:
            self.locks.add('view:false()')
            self.locks.add('search:false()')



    def at_pre_get(self, getter, **kwargs):

        is_stuck = self.stuck_bool

        if is_stuck:
            getter.msg("You cannot pick that up.")
            return False
        else:
            return True

        # attr(attrname, value)

        # print("at_object_creation")

        # print(self.attributes)
        # # Set locks based on weenie props

        # print(WeeniePropBool.Stuck.value)

        # # is_stuck = self.attributes.get(WeeniePropBool.Stuck.value, category="properties")

        # stuck_test = self.stuck_bool

        # print(stuck_test)

        # #print(is_stuck)

        # if stuck_test:
        #     self.locks.add("get:false()")

        # print(self.locks)

    def at_pre_use(self, user, **kwargs):
        pass

    def use(self, user, **kwargs):
        pass

    def at_post_use(self, user, **kwargs):
        pass

    def get_display_name(self, looker=None, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (TypedObject): The object or account that is looking
                at/getting inforamtion for this object. If not given, `.name` will be
                returned, which can in turn be used to display colored data.

        Returns:
            str: A name to display for this object. This can contain color codes and may
                be customized based on `looker`. By default this contains the `.key` of the object,
                followed by the DBREF if this user is privileged to control said object.

        Notes:
            This function could be extended to change how object names appear to users in character,
            but be wary. This function does not change an object's keys or aliases when searching,
            and is expected to produce something useful for builders.

        """

        print(self.name)

        # if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
        #     return f"{self.name}(#{self.id})"
        # return f"{self.name}"

        if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
            return f"{self.name_color}{self.name}(#{self.id})|n"
        return f"{self.name_color}{self.name}|n"

        # if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
        #     return f"{self.name_color}{self.name}(#{self.id})|n"
        # return f"{self.name_color}{self.name}|n"

        # if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
        #     return f"{self.name}(#{self.id})"
        # return self.name

    # def get_numbered_name(self, count, looker, **kwargs):
    #     """
    #     Return the numbered (singular, plural) forms of this object's key. This is by default called
    #     by return_appearance and is used for grouping multiple same-named of this object. Note that
    #     this will be called on *every* member of a group even though the plural name will be only
    #     shown once. Also the singular display version, such as 'an apple', 'a tree' is determined
    #     from this method.

    #     Args:
    #         count (int): Number of objects of this type
    #         looker (Object): Onlooker. Not used by default.

    #     Keyword Args:
    #         key (str): Optional key to pluralize. If not given, the object's `.name` property is
    #             used.

    #     Returns:
    #         tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
    #             including the count.

    #     Examples:
    #         ::
    #             obj.get_numbered_name(3, looker, key="foo") -> ("a foo", "three foos")

    #     """
    #     plural_category = "plural_key"
    #     key = kwargs.get("key", self.name)
    #     key = ansi.ANSIString(key)  # this is needed to allow inflection of colored names
    #     try:
    #         plural = _INFLECT.plural(key, count)
    #         plural = "{} {}".format(_INFLECT.number_to_words(count, threshold=12), plural)
    #     except IndexError:
    #         # this is raised by inflect if the input is not a proper noun
    #         plural = key
    #     singular = _INFLECT.an(key)
    #     if not self.aliases.get(plural, category=plural_category):
    #         # we need to wipe any old plurals/an/a in case key changed in the interrim
    #         self.aliases.clear(category=plural_category)
    #         self.aliases.add(plural, category=plural_category)
    #         # save the singular form as an alias here too so we can display "an egg" and also
    #         # look at 'an egg'.
    #         self.aliases.add(singular, category=plural_category)
    #     return singular, plural

    pass
