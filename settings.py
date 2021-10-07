import logging
from datetime import datetime
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
    from local_settings import BOLD_FONT
except ImportError:
    BOLD_FONT = "/usr/share/fonts/truetype/dejava/DejaVuSans-Bold.ttf"

try:
    from local_settings import MONOSPACE_FONT
except ImportError:
    MONOSPACE_FONT = "/usr/share/fonts/truetype/dejava/DejaVuSansMono.ttf"

try:
    from local_settings import APPS
except ImportError:
    APPS = get_apps()

try:
    from local_settings import TIMEZONE
except ImportError:
    TIMEZONE = datetime.now().astimezone().tzname

try:
    from local_settings import BACKGROUND
except ImportError:
    BACKGROUND = "images/wallpaper.png"

try:
    from local_settings import TEXT_COLOR
except ImportError:
    TEXT_COLOR = "white"

try:
    from local_settings import BACKGROUND_COLOR
except ImportError:
    BACKGROUND_COLOR = "black"

try:
    from local_settings import SPLASH_IMAGE
except ImportError:
    SPLASH_IMAGE = "images/raspberry-pi.png"

try:
    from local_settings import SAVE_SCREENSHOTS
except ImportError:
    SAVE_SCREENSHOTS = False
