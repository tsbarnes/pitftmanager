import importlib
import logging
import time
import sys
from types import ModuleType

import settings
from utils import wrapped_text
from framebuffer import Framebuffer
from apps import AbstractApp, get_apps


class PiTFTManager:
    framebuffer: Framebuffer = Framebuffer(1)
    app_modules: list = []
    apps: list = []
    current_app_module: ModuleType = None
    current_app: AbstractApp = None

    def __init__(self):
        logging.basicConfig(level=settings.LOGLEVEL)
        app_names = settings.APPS
        for name in app_names:
            try:
                module = importlib.import_module(name)
                self.app_modules.append(module)
            except ImportError:
                try:
                    module = importlib.import_module("apps." + name)
                    self.app_modules.append(module)
                except ImportError:
                    logging.error("Couldn't load app '{0}'" % name)

        if len(self.app_modules) < 1:
            logging.error("No apps found, exiting...")
            sys.exit(1)

        for module in self.app_modules:
            self.apps.append(module.App(self.framebuffer))

        self.current_app_module = self.app_modules[0]
        self.current_app = self.apps[0]

    def main_loop(self):
        while True:
            self.current_app.run_once()
            time.sleep(1)


if __name__ == '__main__':
    app = PiTFTManager()
    image = wrapped_text("Starting PiTFT Manager...", app.framebuffer.size, font_size=40, background_color="black")
    app.framebuffer.show(image)
    app.main_loop()
