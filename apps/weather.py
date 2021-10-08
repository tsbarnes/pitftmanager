from apps import AbstractApp
import logging
from libs.weather import Weather, get_weather


logger = logging.getLogger("pitftmanager.apps.weather")


class App(AbstractApp):
    weather: Weather = get_weather()

    def reload(self):
        self.blank()
        self.draw_titlebar("Weather")

        try:
            logo = self.weather.get_icon()
            self.image.paste(logo, (60, 55))

            text = str(self.weather.weather.current.temperature) + '°'
            self.centered_text(text, font_size=80, y=30)

            text = str(self.weather.weather.current.sky_text)
            self.centered_text(text, font_size=40, y=120)

            text = str(self.weather.weather.location_name)
            self.centered_text(text, font_size=40, y=170)

            logger.debug("Sky Code: " + str(self.weather.weather.current.sky_code))
        except AttributeError:
            self.blank()
            text = "No weather information"
            self.centered_text(text, font_size=30, y=120)
