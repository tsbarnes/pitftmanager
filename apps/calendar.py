import logging
from apps import AbstractApp
from libs.calendar import Calendar, get_calendar


class App(AbstractApp):
    calendar: Calendar = get_calendar()

    def reload(self):
        lines = self.calendar.events_as_lines()

        self.blank()

        if len(lines) < 1:
            self.wrapped_text('No current events', (5, 5), font_size=30)
            return

        current_line_height = 5
        for line in lines:
            number_of_lines = self.wrapped_text(line, (5, current_line_height), font_size=20)
            current_line_height += 20 * number_of_lines

    def reload_old(self):
        text = self.calendar.events_as_string()

        self.blank()

        if text != '':
            self.wrapped_text(text, (5, 5), font_size=20)
        else:
            self.wrapped_text('No current events', (5, 5), font_size=25)
