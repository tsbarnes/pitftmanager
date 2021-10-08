from apps import AbstractApp
from libs.calendar import Calendar, get_calendar


class App(AbstractApp):
    calendar: Calendar = get_calendar()
    refresh_interval: int = 0

    def reload(self):
        self.blank()
        self.draw_titlebar("Tasks")

        if len(self.calendar.tasks) < 1:
            self.text("No current tasks", position=(5, 30))
            return

        current_line = 0
        for task in self.calendar.tasks:
            text = str(task['summary'].strip('\n'))
            current_line += self.text(text, font_size=24, position=(5, 30 + current_line * 24), max_lines=2)
            if task.get('due'):
                text = ' -- Due: ' + self.calendar.humanized_datetime(task['due'])
                current_line += self.text(text, font_size=24, position=(5, 30 + current_line * 24), max_lines=1)
