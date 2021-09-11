import platform
import time
import datetime
import humanize

from PIL import Image
from framebuffer import Framebuffer


class PiTFTManager:
    framebuffer = Framebuffer(1)

    def system_info(self):
        self.framebuffer.blank()

        logo = Image.open('raspberry-pi.png')
        logo.thumbnail((50, 50))
        self.framebuffer.image.paste(logo, (5, 5, logo.size[0] + 5, logo.size[1] + 5))

        text = ''

        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            model = model_file.read()
            text += '\t' + model + '\n'

        text += '\tSystem:  ' + platform.system() + '\n'

        dist = " ".join(x for x in platform.dist())
        text += '\tOS:      ' + dist + '\n'

        text += '\tMachine: ' + platform.machine() + '\n'
        text += '\tNode:    ' + platform.node() + '\n'
        text += '\tArch:    ' + platform.architecture()[0] + '\n'

        uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
        text += '\tUptime:  ' + humanize.naturaldelta(uptime)

        self.framebuffer.text(text, fontsize=20)

    def main_loop(self):
        while True:
            time.sleep(1)

            self.framebuffer.redraw_screen()


if __name__ == '__main__':
    app = PiTFTManager()
    app.framebuffer.text("Starting PiTFT Manager...", fontsize=40, background_color="black")
    app.system_info()
    app.main_loop()
