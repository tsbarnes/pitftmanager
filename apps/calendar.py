import logging
from apps import AbstractApp
from libs.calendar import Calendar, get_calendar


class App(AbstractApp):
    calendar: Calendar = get_calendar()

    def reload(self):
        self.blank()
        self.draw_titlebar("Calendar")

        if len(self.calendar.events) < 1:
            self.text('No current events', (5, 30), font_size=30)
            return

        current_line = 0
        for event in self.calendar.events:
            text = ' -- ' + self.calendar.humanized_datetime(event['start']) + ' -- '
            current_line += self.text(text, font_size=24, position=(5, 30 + current_line * 24), max_lines=1)
            text = str(event['summary'])
            current_line += self.text(text, font_size=24, position=(5, 30 + current_line * 24), max_lines=2)
