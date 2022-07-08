from Teletel import Teletel
from views.ViewController import *


class ListViewController(ViewController):

    def __init__(self, baudrate, port):
        super().__init__(baudrate, port)

        self.top_of_page = ()   # x,y position of top of page
        self.displayed_list = []   # current displayed list

    def draw(self):
        super().draw()

        self._minitel.inverse(True)
        self._minitel._print("Résultats de recherche pour:")
        self._minitel.inverse(False)
        self._minitel._print("\"Napoléon Ier, Roi de France et Empereur hihihihih\"\n")
        self._minitel.plot("_", 40)

        self.top_of_page = self._minitel.curpos()

    def print_list(self, list_to_print):
        """
        Print a numerated list

        :param list[str] list_to_print: List of element to print
        """
        self.displayed_list = list_to_print
        for i, elem in enumerate(list_to_print):
            self._print_line(i+1, elem)

        self._minitel.flash()

    def _print_line(self, index, text, reverse=False):
        elem_index = "{})".format(index)

        self._minitel.inverse(not reverse)
        self._minitel._print(elem_index)
        self._minitel.inverse(reverse)

        self._minitel._print(text)
        curPos = self._minitel.curpos()
        self._minitel._del(*curPos)
        self._minitel._print("\n")

    def handle_input(self):
        current_input = self._minitel.get()
        selection = 0
        while current_input != Teletel.ENVOI.value:
            current_input = self._minitel.input(20, 38, 2)
            print(current_input)

    def _draw_footer(self):
        pass


