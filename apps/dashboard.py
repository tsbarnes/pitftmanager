import logging
from datetime import datetime
from apps import AbstractApp
from libs.calendar import Calendar, get_calendar, update_calendar
from libs.weather import Weather, get_weather, update_weather


class App(AbstractApp):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()
        self.draw_titlebar("Dashboard")

        logo = self.weather.get_icon()
        self.image.paste(logo, (20, 35))

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=48, position=(60, 25))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=20, position=(150, 35))

        text = "{0:02d}:{1:02d}".format(datetime.now().hour, datetime.now().minute)
        self.text(text, font_size=20, position=(350, 35))

        self.line((0, 80, self.image.size[0], 80), width=2)

        if len(self.calendar.events) > 0:
            start = self.calendar.standardize_date(self.calendar.events[0]["start"])
            text = ' -- ' + self.calendar.humanized_datetime(start) + ' -- '
            self.text(text, font_size=24, position=(5, 90), color="yellow", max_lines=1)

            text = str(self.calendar.events[0]['summary'])
            self.text(text, font_size=24, position=(5, 120), max_lines=2)

        self.line((0, 190, self.image.size[0], 190), width=2)

        if len(self.calendar.tasks) > 0:
            text = str(self.calendar.tasks[0]['summary'])
            self.text(text, font_size=24, position=(5, 200), max_lines=2)
            if self.calendar.tasks[0].get('due'):
                text = ' - Due: ' + self.calendar.humanized_datetime(self.calendar.tasks[0]['due'])
                self.text(text, font_size=24, position=(5, 230), color="yellow", max_lines=1)

    def touch(self, position: tuple):
        if position[1] in range(0, 70):
            logging.debug("Weather touched")
            self.blank()
            self.centered_text("Please wait...", font_size=50, y=50)
            self.show()
            update_weather()
            self.reload()
            self.show()
        elif position[1] in range(70, 180):
            logging.debug("Calendar touched")
            self.blank()
            self.centered_text("Please wait...", font_size=50, y=50)
            self.show()
            update_calendar()
            self.reload()
            self.show()
        logging.debug("Position {} touched".format(position))
