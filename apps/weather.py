from apps import AbstractApp
import logging
from libs.weather import Weather, get_weather, update_weather


class App(AbstractApp):
    weather: Weather = get_weather()

    def reload(self):
        self.blank()
        self.draw_titlebar("Weather")

        try:
            centered_position: int = round(self.framebuffer.size[0] / 2 - 40)
            box: tuple = (centered_position, 5)

            text = str(self.weather.weather.current.temperature) + '°'
            self.wrapped_text(text, font_size=80, position=(centered_position, 30))

            text = str(self.weather.weather.current.sky_text)
            self.wrapped_text(text, font_size=40, position=(centered_position, 120))

            text = str(self.weather.weather.current.day)
            self.wrapped_text(text, font_size=40, position=(centered_position, 170))

            logging.debug("Sky Code: " + str(self.weather.weather.current.sky_code))
        except AttributeError:
            text = "No weather information"
            self.wrapped_text(text, font_size=30, position=(5, 5))
