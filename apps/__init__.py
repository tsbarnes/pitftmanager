import logging
import pathlib
import os
import inspect
import textwrap
from pathlib import Path
from string import ascii_letters
from typing import Generator
from PIL import Image, ImageDraw, ImageFont
import settings
from framebuffer import Framebuffer


class AbstractApp:
    framebuffer: Framebuffer = None
    image: Image = None
    reload_interval: int = 60
    reload_wait: int = 0

    def __init__(self, fb):
        self.framebuffer = fb
        self.blank()
        self.reload()

    def blank(self):
        if settings.BACKGROUND:
            image: Image = Image.open(settings.BACKGROUND)
            self.image = image.resize(self.framebuffer.size)
        else:
            self.image = Image.new("RGBA", self.framebuffer.size, settings.BACKGROUND_COLOR)

    def wrapped_text(self, text, position=(5, 5), font_name=None, font_size=20, color=None):
        if not font_name:
            font_name = settings.FONT
        if not color:
            color = settings.TEXT_COLOR
        if not self.image:
            raise ValueError("self.image is None")

        font: ImageFont = ImageFont.truetype(font_name, font_size)
        draw: ImageDraw = ImageDraw.Draw(self.image)

        avg_char_width: int = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count: int = int((self.image.size[0] * .95) / avg_char_width)

        scaled_wrapped_text: str = ''
        for line in text.split('\n'):
            scaled_wrapped_text += textwrap.fill(text=line, width=max_char_count) + '\n'
        draw.text(position, scaled_wrapped_text, font=font, fill=color)

    def show(self):
        if not self.image:
            logging.error("App '{0}' called 'show' without an image!".format(self.__module__))
            self.blank()
        self.framebuffer.show(self.image)

    def reload(self):
        raise NotImplementedError()

    def run_iteration(self):
        self.reload_wait += 1
        if not self.image or self.reload_wait >= self.reload_interval:
            if self.image:
                logging.debug("App '{0}' hit auto-reload interval ({1} seconds)".format(
                    type(self).__module__, self.reload_interval))
            self.reload_wait = 0
            self.reload()


def get_apps():
    apps: list = []

    path: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    app_directory: Generator[Path, None, None] = pathlib.Path(path).rglob("*.py")

    for file in app_directory:
        if file.name == "__init__.py":
            continue
        module_name = file.name.split(".")[0]
        logging.debug("Found '{0}' in '{1}'".format(module_name, path))
        apps.append(module_name)

    return apps


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_apps()
