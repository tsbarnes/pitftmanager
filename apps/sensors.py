"""Sensors screen"""
from apps import AbstractApp
import sensors


class App(AbstractApp):
    def __init__(self, fb):
        """
        Initialize sensors library
        """
        sensors.init()
        super().__init__(fb)

    def reload(self):
        self.blank()
        self.draw_titlebar("Sensors")

        current_line = 0
        for chip in sensors.iter_detected_chips():
            current_line += self.text(chip.adapter_name, font_size=50, position=(5, 30 + current_line * 50))

            for feature in chip:
                line = "{}: {}".format(feature.label, feature.get_value())
                current_line += self.text(line, font_size=50, color="yellow", position=(5, 30 + current_line * 50))
