import random
import settings
from apps import AbstractApp


class App(AbstractApp):
    affirmations: list = settings.AFFIRMATIONS
    current_affirmation: str = affirmations[0]
    reload_interval: int = 600

    def get_random_affirmation(self):
        affirmation = random.choice(self.affirmations)
        while affirmation == self.current_affirmation:
            affirmation = random.choice(self.affirmations)
        self.current_affirmation = affirmation
        return affirmation

    def reload(self):
        self.blank()
        self.current_affirmation = self.get_random_affirmation()
        self.wrapped_text(self.current_affirmation, (5, 5), font_size=40)

    def touch(self, position: tuple):
        self.get_random_affirmation()
        self.reload()
        self.show()
