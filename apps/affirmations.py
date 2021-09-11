import random
import settings
from PIL import Image
from apps import AbstractApp
from utils import wrapped_text


class App(AbstractApp):
    affirmations: list = settings.AFFIRMATIONS
    current_affirmation: str = affirmations[0]
    image: Image = None

    def get_random_affirmation(self):
        affirmation = random.choice(self.affirmations)
        while affirmation == self.current_affirmation:
            affirmation = random.choice(self.affirmations)
        self.current_affirmation = affirmation
        return affirmation

    def reload(self):
        self.current_affirmation = self.get_random_affirmation()
        self.image = wrapped_text(self.current_affirmation, self.framebuffer.size, font_size=40)

    def run_iteration(self):
        if not self.image:
            self.reload()
        self.framebuffer.show(self.image)
