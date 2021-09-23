import humanize
import logging
import settings
from PIL import Image, ImageDraw, ImageFont
from apps import AbstractApp
from libs.system import System, get_system


class App(AbstractApp):
    reload_interval = 5
    system: System = get_system()

    def reload(self):
        self.blank()
        self.draw_titlebar("System")

        draw: ImageDraw = ImageDraw.Draw(self.image)
        font: ImageFont = ImageFont.truetype(settings.MONOSPACE_FONT, 25)

        text: str = self.system.model + '\n'

        text += 'System:  ' + self.system.system + '\n'

        text += 'OS:      ' + self.system.dist + '\n'

        text += 'Machine: ' + self.system.machine + '\n'
        text += 'Node:    ' + self.system.node + '\n'
        text += 'Arch:    ' + self.system.arch + '\n'

        text += 'Uptime:  ' + humanize.naturaldelta(self.system.uptime)

        draw.text((5, 120), text, font=font, fill=settings.TEXT_COLOR)

        logo: Image = Image.open('images/raspberry-pi.png')
        logo.thumbnail((80, 80))
        centered_position: int = round(self.framebuffer.size[0] / 2 - 40)
        box: tuple = (centered_position, 30)

        try:
            self.image.paste(logo, box)
        except ValueError:
            logging.error("Failed to paste image")

    def touch(self, position: tuple):
        if position[1] < 50:
            logging.debug("Top of screen touched")
        if position[1] > self.framebuffer.size[1] - 50:
            logging.debug("Bottom of screen touched")
        if position[0] < 50:
            logging.debug("Left of screen touched")
        if position[0] > self.framebuffer.size[0] - 50:
            logging.debug("Right of screen touched")
        logging.debug("System app caught touch: {}".format(position))
