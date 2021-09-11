import logging
from apps import get_apps

try:
    from local_settings import LOGLEVEL
except ImportError:
    LOGLEVEL = logging.INFO

try:
    from local_settings import FONT
except ImportError:
    FONT = "/usr/share/fonts/truetype/dejava/DejaVuSans.ttf"

try:
    from local_settings import MONOSPACE_FONT
except ImportError:
    MONOSPACE_FONT = "/usr/share/fonts/truetype/dejava/DejaVuSansMono.ttf"

try:
    from local_settings import APPS
except ImportError:
    APPS = get_apps()

try:
    from local_settings import AFFIRMATIONS
except ImportError:
    AFFIRMATIONS = [
        "You can do it!",
        "You are safe.",
        "You'll be okay.",
        "Things will get better.",
        "The past can't hurt you anymore.",
    ]