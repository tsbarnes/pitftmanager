from apps import AbstractApp
import python_weather
import asyncio
import settings
import logging


class Weather:
    weather = None

    async def getweather(self):
        client = python_weather.Client(format=settings.WEATHER_FORMAT)
        self.weather = await client.find(settings.WEATHER_CITY)
        await client.close()


class App(AbstractApp):
    weather: Weather = Weather()
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    def __init__(self, fb):
        self.loop.run_until_complete(self.weather.getweather())
        super().__init__(fb)

    def reload(self):
        self.blank()

        # logo = Image.open(settings.LOGO)
        # self.image.paste(logo, (100, 5))

        centered_position: int = round(self.framebuffer.size[0] / 2 - 40)
        box: tuple = (centered_position, 5)

        text = str(self.weather.weather.current.temperature) + '°'
        self.wrapped_text(text, font_size=80, position=(centered_position, 10))

        text = str(self.weather.weather.current.sky_text)
        self.wrapped_text(text, font_size=40, position=(centered_position, 100))

        text = str(self.weather.weather.current.day)
        self.wrapped_text(text, font_size=40, position=(centered_position, 150))

        logging.debug("Sky Code: " + str(self.weather.weather.current.sky_code))

    def run_iteration(self):
        if self.reload_wait >= self.reload_interval:
            self.loop.run_until_complete(self.weather.getweather())

        super().run_iteration()
