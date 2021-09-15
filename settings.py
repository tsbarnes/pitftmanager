import logging
import python_weather
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

try:
    from local_settings import CALENDAR_URLS
except ImportError:
    CALENDAR_URLS = None

try:
    from local_settings import CALENDAR_REFRESH
except ImportError:
    CALENDAR_REFRESH = 900

try:
    from local_settings import TIMEZONE
except ImportError:
    TIMEZONE = datetime.now().astimezone().tzname

try:
    from local_settings import BACKGROUND
except ImportError:
    BACKGROUND = None

try:
    from local_settings import TEXT_COLOR
except ImportError:
    TEXT_COLOR = "white"

try:
    from local_settings import BACKGROUND_COLOR
except ImportError:
    BACKGROUND_COLOR = "black"


try:
    from local_settings import WEATHER_FORMAT
except ImportError:
    WEATHER_FORMAT = python_weather.IMPERIAL

try:
    from local_settings import WEATHER_CITY
except ImportError:
    WEATHER_CITY = "Richmond, VA"

try:
    from local_settings import WEATHER_REFRESH
except ImportError:
    WEATHER_REFRESH = 900
