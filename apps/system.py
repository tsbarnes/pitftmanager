import datetime
import platform
import time
import humanize
from framebuffer import Framebuffer
from PIL import Image, ImageDraw, ImageFont
from apps import AbstractApp


class App(AbstractApp):
    framebuffer: Framebuffer = None

    def __init__(self, fb):
        self.framebuffer = fb

    def run_once(self):
        image = Image.new("RGBA", self.framebuffer.size, "black")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)

        text = ''

        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            model = model_file.read()
            text += model + '\n'

        text += 'System:  ' + platform.system() + '\n'

        dist = " ".join(x for x in platform.dist())
        text += 'OS:      ' + dist + '\n'

        text += 'Machine: ' + platform.machine() + '\n'
        text += 'Node:    ' + platform.node() + '\n'
        text += 'Arch:    ' + platform.architecture()[0] + '\n'

        uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
        text += 'Uptime:  ' + humanize.naturaldelta(uptime)

        draw.text((5, 55), text, font=font, fill="white")

        logo = Image.open('raspberry-pi.png')
        logo.thumbnail((50, 50))
        image.paste(logo)

        self.framebuffer.show(image)
