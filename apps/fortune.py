import subprocess
import logging
from PIL import Image
from apps import AbstractApp
from utils import wrapped_text


class App(AbstractApp):
    output: str = ''
    image: Image = None

    def __init__(self, fb):
        super().__init__(fb)
        self.reload()

    def reload(self):
        try:
            child = subprocess.Popen(['/usr/games/fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.output = child.stdout.read().decode().replace('\n', ' ')
        except OSError:
            logging.error("couldn't run application 'fortune'")
            self.output = ''
        self.image = wrapped_text(self.output, self.framebuffer.size, font_size=16)

    def run_iteration(self):
        self.framebuffer.show(self.image)
