import logging
import pathlib
import os
import inspect
from PIL import Image
from framebuffer import Framebuffer


class AbstractApp:
    framebuffer: Framebuffer = None
    image: Image = None

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
        if not self.image:
            self.reload()
        self.show()


def get_apps():
    apps = []

    path: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    app_directory = pathlib.Path(path).rglob("*.py")

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
