from apps import AbstractApp
from libs.calendar import Calendar, get_calendar


class App(AbstractApp):
    calendar: Calendar = get_calendar()
    refresh_interval: int = 0

    def reload(self):
        self.blank()

        text = self.calendar.tasks_as_string()
        if text != '':
            self.wrapped_text(text, (5, 5), font_size=20)
        else:
            self.wrapped_text('No current tasks', (5, 5), font_size=25)
