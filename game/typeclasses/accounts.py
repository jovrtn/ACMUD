"""
Account

The Account represents the game "account" and each login has only one
Account object. An Account is what chats on default channels but has no
other in-game-world existence. Rather the Account puppets Objects (such
as Characters) in order to actually participate in the game world.


Guest

Guest accounts are simple low-level accounts that are created/deleted
on the fly and allows users to test the game without the commitment
of a full registration. Guest accounts are deactivated by default; to
activate them, add the following line to your settings file:

    GUEST_ENABLED = True

You will also need to modify the connection screen to reflect the
possibility to connect with a guest account. The setting file accepts
several more options for customizing the Guest account system.

"""

from django.conf import settings
from evennia.utils import evtable

from evennia.utils.utils import (
    is_iter,
    lazy_property,
    make_iter,
    to_str,
    variable_from_module,
)

from evennia.accounts.accounts import DefaultAccount, DefaultGuest


class Account(DefaultAccount):
    """
    This class describes the actual OOC account (i.e. the user connecting
    to the MUD). It does NOT have visual appearance in the game world (that
    is handled by the character which is connected to this). Comm channels
    are attended/joined using this object.

    It can be useful e.g. for storing configuration options for your game, but
    should generally not hold any character-related info (that's best handled
    on the character level).

    Can be set using BASE_ACCOUNT_TYPECLASS.


    * available properties

     key (string) - name of account
     name (string)- wrapper for user.username
     aliases (list of strings) - aliases to the object. Will be saved to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     user (User, read-only) - django User authorization object
     obj (Object) - game object controlled by account. 'character' can also be used.
     sessions (list of Sessions) - sessions connected to this account
     is_superuser (bool, read-only) - if the connected user is a superuser

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().

    * Helper methods

     msg(text=None, **kwargs)
     execute_cmd(raw_string, session=None)
     search(ostring, global_search=False, attribute_name=None, use_nicks=False, location=None, ignore_errors=False, account=False)
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hook methods (when re-implementation, remember methods need to have self as first arg)

     basetype_setup()
     at_account_creation()

     - note that the following hooks are also found on Objects and are
       usually handled on the character level:

     at_init()
     at_cmdset_get(**kwargs)
     at_first_login()
     at_post_login(session=None)
     at_disconnect()
     at_message_receive()
     at_message_send()
     at_server_reload()
     at_server_shutdown()

    """

    ooc_appearance_template = """
--------------------------------------------------------------------

  |wAsheron's Call MUD|n
  {header}

--------------------------------------------------------------------
  
  |wOptions|n

{options}

  |wCharacters|n ({num_chars}/{max_chars})

{footer}

--------------------------------------------------------------------
""".strip()

    def at_look(self, target=None, session=None, **kwargs):
        """
        Called when this object executes a look. It allows to customize
        just what this means.

        Args:
            target (Object or list, optional): An object or a list
                objects to inspect. This is normally a list of characters.
            session (Session, optional): The session doing this look.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Returns:
            look_string (str): A prepared look string, ready to send
                off to any recipient (usually to ourselves)

        """

        _MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS

        if target and not is_iter(target):
            # single target - just show it
            if hasattr(target, "return_appearance"):
                return target.return_appearance(self)
            else:
                return f"{target} has no in-game appearance."

        # multiple targets - this is a list of characters
        characters = list(tar for tar in target if tar) if target else []
        ncars = len(characters)
        sessions = self.sessions.all()
        nsess = len(sessions)

        if not nsess:
            # no sessions, nothing to report
            return ""

        # header text
        txt_header = f"|wAccount:|n |g{self.name}|n"

        # # sessions
        # sess_strings = []
        # for isess, sess in enumerate(sessions):
        #     ip_addr = sess.address[0] if isinstance(
        #         sess.address, tuple) else sess.address
        #     addr = f"{sess.protocol_key} ({ip_addr})"
        #     sess_str = (
        #         f"|w* {isess + 1}|n"
        #         if session and session.sessid == sess.sessid
        #         else f"  {isess + 1}"
        #     )

        #     sess_strings.append(f"{sess_str} {addr}")

        # txt_sessions = "|wConnected session(s):|n\n" + "\n".join(sess_strings)

        max_chars = (
                "unlimited"
                if self.is_superuser or _MAX_NR_CHARACTERS is None
                else _MAX_NR_CHARACTERS
            )


        # if not characters:
        #     txt_characters = "You don't have a character yet. Use |wcharcreate|n."
        # else:
        #     max_chars = (
        #         "∞"
        #         if self.is_superuser or _MAX_NR_CHARACTERS is None
        #         else _MAX_NR_CHARACTERS
        #     )

        #     char_strings = []
            

            # for char in characters:



            #     csessions = char.sessions.all()
            #     if csessions:
            #         for sess in csessions:
            #             # character is already puppeted
            #             sid = sess in sessions and sessions.index(sess) + 1
            #             if sess and sid:
            #                 char_strings.append(
            #                     f" - |G{char.name}|n [{
            #                         ', '.join(char.permissions.all())}] "
            #                     f"(played by you in session {sid})"
            #                 )
            #             else:
            #                 char_strings.append(
            #                     f" - |R{char.name}|n [{
            #                         ', '.join(char.permissions.all())}] "
            #                     "(played by someone else)"
            #                 )
            #     else:
            #         # character is "free to puppet"
            #         char_strings.append(
            #             f" - {char.name} [{', '.join(char.permissions.all())}]")

            # txt_characters = (
            #     f"Available character(s) ({
            #         ncars}/{max_chars}, |wic <name>|n to play):|n\n"
            #     + "\n".join(char_strings)
            # )



        indentation = 2
        width = 65
        options_table = evtable.EvTable("|wCommand|n", "|wDescription|n", border="cells", width=width)
        # table.add_column("This is long data", "This is even longer data")
        options_table.add_row("login <name>", "Log in to a character")
        options_table.add_row("createchar", "Create a new character")
        options_table.add_row("deletechar <name>", "Delete a character")
        options_table.add_row("disconnect", "Disconnect from the server")
        options_table.add_row("help", "See all commands")
        # options_table.add_row("Maethor")

       

        char_string = ""

        if not characters:
            char_string = "  You have no characters.\rUse |wcreatechar|n to get started."
        else:
            
            character_table = evtable.EvTable(header=False, border="cells", width=width)
            
            for char in characters:

                char_string = ""
                permission_symbol = ""
                is_admin = char.permissions.check("Admin", "Developer")
                is_builder = char.permissions.check("Admin", "Developer")

                if (is_builder): permission_symbol = "@"
                if (is_admin): permission_symbol = "+"
                

                char_string = permission_symbol + char_string + char.name


                #character_table.add_row(f"|G{char.name}|n [{', '.join(char.permissions.all())}]")

                character_table.add_row(char_string)

                char_string = "\n".join(" " * indentation + line for line in str(character_table).splitlines())
            

     
        # Add leading spaces for indentation
        options_table_string = "\n".join(" " * indentation + line for line in str(options_table).splitlines())
        

        return self.ooc_appearance_template.format(
            header=txt_header,
            max_chars=max_chars,
            num_chars=ncars,
            options=options_table_string,
            footer=char_string,
        )

    pass
