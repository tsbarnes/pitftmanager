import importlib
import logging
import time
import sys
from types import ModuleType
import posix_ipc
import settings
from framebuffer import Framebuffer
from apps import AbstractApp
from libs.calendar import Calendar, get_calendar
from pitft_touchscreen import pitft_touchscreen, get_pixels_from_coordinates


class PiTFTManager:
    framebuffer: Framebuffer = Framebuffer(1)
    app_modules: list = []
    apps: list = []
    current_app_index: int = 0
    current_app_module: ModuleType = None
    current_app: AbstractApp = None
    calendar: Calendar = get_calendar()
    pitft_touchscreen = pitft_touchscreen()
    touch_x: int = 0
    touch_y: int = 0

    def __init__(self):
        self.mq = posix_ipc.MessageQueue("/pitftmanager_ipc", flags=posix_ipc.O_CREAT)
        self.mq.block = False

        self.pitft_touchscreen.start()

        app_names = settings.APPS
        for name in app_names:
            self.load_app(name)

        if len(self.app_modules) < 1:
            logging.error("No apps found, exiting...")
            sys.exit(1)

        for module in self.app_modules:
            self.apps.append(module.App(self.framebuffer))

        self.switch_app(0)

        logging.info("PiTFT Size: {0}x{1}".format(self.framebuffer.size[0], self.framebuffer.size[1]))

        self.calendar.get_latest_events()

    def load_app(self, name):
        try:
            module = importlib.import_module(name)
            self.app_modules.append(module)
        except ImportError:
            try:
                module = importlib.import_module("apps." + name)
                self.app_modules.append(module)
            except ImportError:
                logging.error("Couldn't load app '{0}'" % name)

    def switch_app(self, index: int):
        self.current_app_index = index % len(self.apps)
        self.current_app_module = self.app_modules[self.current_app_index]
        self.current_app = self.apps[self.current_app_index]

    def switch_app_by_name(self, name: str):
        index = 0
        for app in self.apps:
            if app.__module__ == name:
                break
            if app.__module__ == "apps." + name:
                break
            index += 1

        if index >= len(self.apps):
            logging.error("App '{0}' not found")
            return

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
                    self.switch_app_by_name(args)
                elif command == "reload":
                    self.current_app.reload()
                elif command == "exit":
                    logging.info("Got 'exit' command, quitting...")
                    sys.exit(0)
                elif command == "load_app":
                    logging.info("Loading app '{0}'...".format(parts[1]))
                    self.load_app(parts[1])
                elif command == "remove_app":
                    logging.info("Removing app '{0}'...".format(parts[1]))
                    raise NotImplementedError()
                else:
                    logging.warning("Unrecognized command: " + command)

            while not self.pitft_touchscreen.queue_empty():
                for event in self.pitft_touchscreen.get_event():
                    if event['touch'] == 1 and self.touch_x == 0:
                        self.touch_x = event['x']
                        self.touch_y = event['y']
                    elif event['touch'] == 0:
                        position = get_pixels_from_coordinates(self.framebuffer, (self.touch_x, self.touch_y))
                        self.current_app.touch(position)
                        self.touch_x = 0
                        self.touch_y = 0

            self.calendar.refresh_interval -= 1
            if self.calendar.refresh_interval <= 0:
                self.calendar.refresh_interval = settings.CALENDAR_REFRESH
                self.calendar.get_latest_events()

            for app in self.apps:
                app.run_iteration()
            self.current_app.show()
            time.sleep(1)


if __name__ == '__main__':
    print("Starting PiTFT Manager...")
    print("Log Level: " + logging.getLevelName(settings.LOGLEVEL))
    logging.basicConfig(level=settings.LOGLEVEL)

    app = PiTFTManager()

    app.framebuffer.blank()
    # image = wrapped_text("Starting PiTFT Manager...", app.framebuffer.size,
    #                      font_name=settings.FONT, font_size=40, background_color="black")
    # app.framebuffer.show(image)

    app.main_loop()
