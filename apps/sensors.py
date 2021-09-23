"""Sensors screen"""
from apps import AbstractApp
import sensors
from libs.system import System, get_system


class App(AbstractApp):
    system: System = get_system()

    def __init__(self, fb):
        """
        Initialize sensors library
        """
        sensors.init()
        super().__init__(fb)

    def reload(self):
        self.blank()
        self.draw_titlebar("Sensors")

        text = "Temperature: " + str(self.system.temperature) + '\n'
        text += "Voltage:     " + str(self.system.voltage)

        self.text(text, position=(5, 30))
