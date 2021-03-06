import humanize
import logging
import settings
from PIL import Image, ImageDraw, ImageFont
from apps import AbstractApp
from libs.system import System, get_system


logger = logging.getLogger("pitftmanager.apps.system")


class App(AbstractApp):
    reload_interval = 5
    system: System = get_system()

    def reload(self):
        self.blank()
        self.draw_titlebar("System")

        draw: ImageDraw = ImageDraw.Draw(self.image)
        font: ImageFont = ImageFont.truetype(settings.MONOSPACE_FONT, 24)

        text: str = self.system.model + '\n'

        text += 'OS:       ' + self.system.dist + '\n'

        text += 'Machine:  ' + self.system.machine + '\n'
        text += 'CPU Temp: ' + str(round(self.system.temperature)) + '°C\n'

        text += 'Node:     ' + self.system.node + '\n'
        text += 'Local IP: ' + self.system.local_ipv4_address + '\n'

        text += 'Uptime:   ' + humanize.naturaldelta(self.system.uptime)

        draw.text((5, 120), text, font=font, fill=settings.TEXT_COLOR)

        logo: Image = Image.open(self.system.icon)
        logo.thumbnail((80, 80))
        centered_position: int = round(self.framebuffer.size[0] / 2 - 40)
        box: tuple = (centered_position, 30)

        try:
            self.image.paste(logo, box)
        except ValueError:
            logger.error("Failed to paste image")

    def touch(self, position: tuple):
        if position[1] < 50:
            logger.debug("Top of screen touched")
        if position[1] > self.framebuffer.size[1] - 50:
            logger.debug("Bottom of screen touched")
        if position[0] < 50:
            logger.debug("Left of screen touched")
        if position[0] > self.framebuffer.size[0] - 50:
            logger.debug("Right of screen touched")
        logger.debug("System app caught touch: {}".format(position))
