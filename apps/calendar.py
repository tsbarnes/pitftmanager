from apps import AbstractApp
from libs.calendar import Calendar, get_calendar


class App(AbstractApp):
    calendar: Calendar = get_calendar()

    def reload(self):
        text = self.calendar.events_as_string()

        self.blank()

        if text != '':
            self.wrapped_text(text, (5, 5), font_size=20)
        else:
            self.wrapped_text('No current events', (5, 5), font_size=25)
