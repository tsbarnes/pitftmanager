import importlib
import logging
import time
import sys
from types import ModuleType
import posix_ipc
import settings
from utils import wrapped_text
from framebuffer import Framebuffer
from apps import AbstractApp


class PiTFTManager:
    framebuffer: Framebuffer = Framebuffer(1)
    app_modules: list = []
    apps: list = []
    current_app_index: int = 0
    current_app_module: ModuleType = None
    current_app: AbstractApp = None

    def __init__(self):
        self.mq = posix_ipc.MessageQueue("/pitftmanager_ipc", flags=posix_ipc.O_CREAT)
        self.mq.block = False

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

        self.switch_app(0)

    def switch_app(self, index):
        self.current_app_index = index % len(self.apps)
        self.current_app_module = self.app_modules[self.current_app_index]
        self.current_app = self.apps[self.current_app_index]

    def previous_app(self):
        self.switch_app(self.current_app_index - 1)

    def next_app(self):
        self.switch_app(self.current_app_index + 1)

    def main_loop(self):
        while True:
            try:
                message = self.mq.receive(timeout=10)
            except posix_ipc.BusyError:
                message = None

            if message:
                parts = message[0].decode().split()
                command = parts[0]
                args = " ".join(parts[1:])

                logging.info("Received IPC command: " + command)

                if command == "previous":
                    self.previous_app()
                elif command == "next":
                    self.next_app()
                elif command == "switch_app":
                    self.switch_app(args)
                elif command == "reload":
                    self.current_app.reload()
                elif command == "exit":
                    logging.info("Got 'exit' command, quitting...")
                    sys.exit(0)
                else:
                    logging.warning("Unrecognized command: " + command)

            self.current_app.run_iteration()
            time.sleep(1)


if __name__ == '__main__':
    print("Starting PiTFT Manager...")
    print("Log Level: " + logging.getLevelName(settings.LOGLEVEL))
    logging.basicConfig(level=settings.LOGLEVEL)

    app = PiTFTManager()
    image = wrapped_text("Starting PiTFT Manager...", app.framebuffer.size, font_size=40, background_color="black")
    app.framebuffer.show(image)

    app.main_loop()
