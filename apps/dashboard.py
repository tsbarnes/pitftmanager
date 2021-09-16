from apps import AbstractApp
from libs.calendar import Calendar, get_calendar, update_calendar
from libs.weather import Weather, get_weather, update_weather


class App(AbstractApp):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()
        self.blank()

        # logo = self.weather.get_icon()
        # self.image.paste(logo, (20, 20))

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=48, position=(60, 5))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=14, position=(150, 20))

        start = self.calendar.standardize_date(self.calendar.events[0]["start"])
        text = self.calendar.humanized_datetime(start)
        self.text(text, font_size=16, position=(5, 60))

        text = str(self.calendar.events[0]['summary'])
        self.text(text, font_size=14, position=(5, 80), wrap=True)

    def touch(self, position: tuple):
        """
        Called when the user taps the screen while the app is active
        :param position: tuple coordinates (in pixels) of the tap
        :return: None
        """
        pass