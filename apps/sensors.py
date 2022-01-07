"""Sensors screen"""
from apps import AbstractApp
from libs.system import System, get_system


class App(AbstractApp):
    system: System = get_system()

    def reload(self):
        self.blank()
        self.draw_titlebar("Sensors")

        text = "Temperature: " + str(self.system.temperature)

        self.text(text, position=(5, 30))
