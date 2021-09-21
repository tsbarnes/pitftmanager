from PIL import Image
from htmlwebshot import WebShot

from apps import AbstractApp

try:
    from local_settings import WEBVIEW_URL
except ImportError:
    WEBVIEW_URL = "http://tsbarnes.com/"


class App(AbstractApp):
    webshot: WebShot = WebShot()

    def reload(self):
        size = self.framebuffer.size
        self.image = Image.open(self.webshot.create_pic(url=WEBVIEW_URL, size=(size[1], size[0])))

    def run_iteration(self):
        super().run_iteration()
