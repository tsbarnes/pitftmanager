import logging
from apps import AbstractApp
from libs.calendar import Calendar, get_calendar, update_calendar
from libs.weather import Weather, get_weather, update_weather


class App(AbstractApp):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()

        logo = self.weather.get_icon()
        self.image.paste(logo, (20, 20))

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=48, position=(60, 5))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=20, position=(150, 20))

        self.line((0, 60, self.image.size[0], 60), width=2)

        if len(self.calendar.events) > 0:
            start = self.calendar.standardize_date(self.calendar.events[0]["start"])
            text = self.calendar.humanized_datetime(start)
            self.text(text, font_size=24, position=(5, 60), color="orange")

            text = str(self.calendar.events[0]['summary'])
            self.text(text, font_size=24, position=(5, 90), wrap=True, max_lines=2)

        self.line((0, 160, self.image.size[0], 160), width=2)

        if len(self.calendar.tasks) > 0:
            text = str(self.calendar.tasks[0]['summary'])
            self.text(text, font_size=24, position=(5, 170), wrap=True, max_lines=2)

    def touch(self, position: tuple):
        if position[0] in range(0, 60):
            if position[1] in range(0, 60):
                logging.debug("Weather icon touched")
        logging.debug("Position {} touched".format(position))
