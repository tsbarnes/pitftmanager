import importlib
import logging
import time
import settings
from utils import wrapped_text
from framebuffer import Framebuffer


class PiTFTManager:
    framebuffer: Framebuffer = Framebuffer(1)

    def __init__(self):
        logging.basicConfig(level=settings.LOGLEVEL)
        self.current_app_module = importlib.import_module("apps.system")
        self.current_app = self.current_app_module.App(self.framebuffer)

    def main_loop(self):
        while True:
            self.current_app.run_once()
            time.sleep(1)


if __name__ == '__main__':
    app = PiTFTManager()
    image = wrapped_text("Starting PiTFT Manager...", app.framebuffer.size, font_size=40, background_color="black")
    app.framebuffer.show(image)
    app.main_loop()
