import logging
import pathlib
import os
import inspect
from pathlib import Path
from typing import Generator

from PIL import Image
from framebuffer import Framebuffer


class AbstractApp:
    framebuffer: Framebuffer = None
    image: Image = None
    reload_interval: int = 60
    reload_wait: int = 0

    def __init__(self, fb):
        self.framebuffer = fb
        self.image = Image.new("RGBA", self.framebuffer.size, 0)
        self.reload()

    def blank(self):
        self.image = Image.new("RGBA", self.framebuffer.size, 0)

    def show(self):
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
