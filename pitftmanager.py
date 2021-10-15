import importlib
import logging
import time
import sys
import signal
from types import ModuleType
import posix_ipc
from PIL import Image

import settings
from libs.framebuffer import Framebuffer
from apps import AbstractApp
from libs.calendar import Calendar, get_calendar
from libs.weather import Weather, get_weather, update_weather
from libs.pitfttouchscreen import PiTFTTouchscreen, get_pixels_from_coordinates


logger = logging.getLogger("pitftmanager")


class PiTFTManager:
    framebuffer: Framebuffer = Framebuffer(1)
    app_modules: list = []
    apps: list = []
    current_app_index: int = 0
    current_app_module: ModuleType = None
    current_app: AbstractApp = None
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()
    pitft_touchscreen = PiTFTTouchscreen()
    touch_x: int = 0
    touch_y: int = 0
    full_second: bool = False

    def __init__(self):
        self.framebuffer.start()

        image: Image = Image.open(settings.SPLASH_IMAGE)
        self.framebuffer.show(image.resize(self.framebuffer.size))

        self.mq = posix_ipc.MessageQueue("/pitftmanager_ipc", flags=posix_ipc.O_CREAT)
        self.mq.block = False

        self.pitft_touchscreen.start()

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)
        signal.signal(signal.SIGHUP, self.quit)

        self.calendar.get_latest_events()
        update_weather()
        self.calendar.start()
        self.weather.start()

        app_names = settings.APPS
        for name in app_names:
            self.load_app(name)

        if len(self.app_modules) < 1:
            logger.error("No apps found, exiting...")
            sys.exit(1)

        for module in self.app_modules:
            this_app = module.App(self.framebuffer)
            self.apps.append(this_app)

        self.switch_app(0)

        logger.info("PiTFT Size: {0}x{1}".format(self.framebuffer.size[0], self.framebuffer.size[1]))

    def quit(self, *args):
        logger.info("PiTFT Manager quitting gracefully...")
        self.framebuffer.blank()
        self.framebuffer.join()
        exit(0)

    def load_app(self, name):
        try:
            module = importlib.import_module("apps." + name)
            self.app_modules.append(module)
        except ImportError:
            try:
                module = importlib.import_module(name)
                self.app_modules.append(module)
            except ImportError:
                logger.error("Couldn't load app '{0}'" % name)

    def remove_app(self, name):
        index = 0
        for app in self.apps:
            if app.__module__ == name:
                break
            if app.__module__ == "apps." + name:
                break
            index += 1

        if index >= len(self.apps):
            logger.error("App '{0}' not found")
            return

        self.apps.pop(index)
        self.app_modules.pop(index)

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
            logger.error("App '{0}' not found")
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

                logger.info("Received IPC command: " + command)

                if command == "previous":
                    self.previous_app()
                elif command == "next":
                    self.next_app()
                elif command == "switch_app":
                    self.switch_app_by_name(args)
                elif command == "reload":
                    self.current_app.reload()
                elif command == "exit":
                    logger.info("Got 'exit' command, quitting...")
                    sys.exit(0)
                elif command == "load_app":
                    logger.info("Loading app '{0}'...".format(parts[1]))
                    self.load_app(parts[1])
                elif command == "remove_app":
                    logger.info("Removing app '{0}'...".format(parts[1]))
                    self.remove_app(parts[1])
                else:
                    logger.warning("Unrecognized command: " + command)

            while not self.pitft_touchscreen.queue_empty():
                for event in self.pitft_touchscreen.get_event():
                    if event['touch'] == 1 and self.touch_x == 0 and self.touch_y == 0:
                        self.touch_x = event['x']
                        self.touch_y = event['y']
                    elif event['touch'] == 0:
                        if event['y'] > self.touch_y + 250:
                            self.previous_app()
                        elif event['y'] < self.touch_y - 250:
                            self.next_app()
                        # elif event['y'] > self.touch_y + 100:
                        #     self.current_app.swipe("down")
                        # elif event['y'] < self.touch_y - 100:
                        #     self.current_app.swipe("up")
                        else:
                            position = get_pixels_from_coordinates(self.framebuffer, (self.touch_x, self.touch_y))
                            self.current_app.touch(position)
                        self.touch_x = 0
                        self.touch_y = 0

            if self.full_second:
                self.full_second = False
                for this_app in self.apps:
                    this_app.run_iteration()
            else:
                self.full_second = True

            self.current_app.show()
            time.sleep(0.5)


if __name__ == '__main__':
    logging.basicConfig(level=settings.LOGLEVEL)
    logger.info("Starting PiTFT Manager...")
    logger.info("Log Level: " + logging.getLevelName(settings.LOGLEVEL))

    app = PiTFTManager()
    app.main_loop()
