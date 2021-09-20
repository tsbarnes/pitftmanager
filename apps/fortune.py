import subprocess
import logging
from apps import AbstractApp


class App(AbstractApp):
    output: str = ''
    reload_interval: int = 600

    def reload(self):
        self.blank()
        self.draw_titlebar("Fortune")
        try:
            child = subprocess.Popen(['/usr/games/fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.output = child.stdout.read().decode().replace('\n', ' ')
        except OSError:
            logging.error("couldn't run application 'fortune'")
            self.output = ''
        self.wrapped_text(self.output, (5, 30), font_size=16)

    def touch(self, position: tuple):
        self.reload()
        self.show()
