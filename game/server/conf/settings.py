r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Asheron's Call MUD"
MULTISESSION_MODE = 0
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
AUTO_PUPPET_ON_LOGIN = False
GUEST_ENABLED = False
MAX_NR_CHARACTERS = 11

DEFAULT_CHANNELS = [
    {
        "key": "General",
        "aliases": ("cg",),
        "desc": "General discussion",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
    {
        "key": "Trade",
        "aliases": ("ct",),
        "desc": "In-game trade discussion",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
    {
        "key": "LFG",
        "aliases": ("clfg",),
        "desc": "Looking for group",
        "locks": "control:perm(Admin);listen:all();send:all()",
    }
]


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
