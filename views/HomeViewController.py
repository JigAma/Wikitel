from Teletel import Teletel
from views.ViewController import *


class HomeViewController(ViewController):

    def __init__(self, baudrate, port):
        super().__init__(baudrate, port)

    def draw(self):
        super().draw()
        self._minitel.xdraw('ecrans/home.vdt')

        self._minitel.resetzones()
        self._minitel.zone(13, 15, 10, '', self._minitel.BLANC)

    def get_searchtext_input(self):
        text_input, key_pressed = self._minitel.input(13, 15, 10, '')

        if key_pressed == Teletel.ENVOI.value:
            return text_input

        if key_pressed == Teletel.REPETITION.value:
            self.draw()
            return self.get_searchtext_input()

        return key_pressed
