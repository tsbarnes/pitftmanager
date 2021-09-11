import importlib
import time
from framebuffer import Framebuffer


class PiTFTManager:
    framebuffer: Framebuffer = Framebuffer(1)

    def __init__(self):
        self.current_app_module = importlib.import_module("apps.system")
        self.current_app = self.current_app_module.App(self.framebuffer)

    def main_loop(self):
        while True:
            self.current_app.run_once()
            time.sleep(1)


if __name__ == '__main__':
    app = PiTFTManager()
    app.framebuffer.text("Starting PiTFT Manager...", fontsize=40, background_color="black")
    app.main_loop()
