import subprocess
import logging
from apps import AbstractApp
from utils import wrapped_text


class App(AbstractApp):
    output: str = ''

    def reload(self):
        try:
            child = subprocess.Popen(['/usr/games/fortune', '-a'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.output = child.stdout.read().decode().replace('\n', ' ')
        except OSError:
            logging.error("couldn't run application 'fortune'")
            self.output = ''
        self.image = wrapped_text(self.output, self.framebuffer.size, font_size=16)
