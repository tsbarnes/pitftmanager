import datetime
import platform
import time
import humanize
import logging
import settings
import distro
from PIL import Image, ImageDraw, ImageFont
from apps import AbstractApp


class App(AbstractApp):
    def reload(self):
        self.blank()
        draw: ImageDraw = ImageDraw.Draw(self.image)
        font: ImageFont = ImageFont.truetype(settings.MONOSPACE_FONT, 25)

        text: str = ''

        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            model: str = model_file.read()
            text += model + '\n'

        text += 'System:  ' + platform.system() + '\n'

        dist = "{0} {1}".format(distro.name(), distro.version())
        text += 'OS:      ' + dist + '\n'

        text += 'Machine: ' + platform.machine() + '\n'
        text += 'Node:    ' + platform.node() + '\n'
        text += 'Arch:    ' + platform.architecture()[0] + '\n'

        uptime: datetime.timedelta = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
        text += 'Uptime:  ' + humanize.naturaldelta(uptime)

        draw.text((5, 90), text, font=font, fill=settings.TEXT_COLOR)

        logo: Image = Image.open('raspberry-pi.png')
        logo.thumbnail((80, 80))
        centered_position: int = round(self.framebuffer.size[0] / 2 - 40)
        box: tuple = (centered_position, 5)

        try:
            self.image.paste(logo, box)
        except ValueError:
            logging.error("Failed to paste image")

    def touch(self, event: dict):
        pass
