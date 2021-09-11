import logging
import pathlib
import os
import inspect
from framebuffer import Framebuffer


class AbstractApp:
    framebuffer: Framebuffer = None

    def __init__(self, fb):
        self.framebuffer = fb

    def reload(self):
        pass

    def run_iteration(self):
        raise NotImplementedError()


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
