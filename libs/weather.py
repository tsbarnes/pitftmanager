import python_weather
import asyncio
import settings


class Weather:
    """
    This class provides access to the weather info
    """
    weather = None
    refresh_interval: int = settings.WEATHER_REFRESH

    async def update(self):
        """
        Update the weather info
        :return: None
        """
        client = python_weather.Client(format=settings.WEATHER_FORMAT)
        self.weather = await client.find(settings.WEATHER_CITY)
        await client.close()


weather: Weather = Weather()


def get_weather():
    """
    Get the main weather object
    :return: Weather
    """
    return weather


def update_weather():
    """
    Update the weather info
    :return: None
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(weather.update())
