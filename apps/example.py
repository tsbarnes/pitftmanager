"""Example app to show how to make them"""
from apps import AbstractApp


class Example:
    """
    Just another class, feel free to make it do whatever you want
    """
    def foobar(self) -> str:
        """
        This method just returns some text, yours can do anything you want
        :return: str
        """
        return "Hello World!"


class App(AbstractApp):
    """
    This class provides the app methods needed by PiTFT Manager
    """

    # Add an instance of our Example class
    example: Example = Example()

    def reload(self):
        """
        This method should draw the contents of the app to self.image
        """

        # self.blank() resets self.image to a blank image
        self.blank()

        # self.text(text) draws the text to self.image
        # Optional parameters include font, font_size, position, and color
        self.text(self.example.foobar(), font_size=40, position=(50, 50))

    def run_iteration(self):
        """
        This method is optional, and will be run once per cycle
        """
        # Do whatever you need to do, but try to make sure it doesn't take too long

        # This line is very important, it keeps the auto reload working
        super().run_iteration()

    def touch(self, position: tuple):
        """
        Called when the user taps the screen while the app is active
        :param position: tuple coordinates (in pixels) of the tap
        :return: None
        """
        pass
