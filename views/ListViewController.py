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

        for i, elem in enumerate(list_to_print):
            elem_index = "{})".format(i + 1)
            # printedThisLoop = len(toPrint) + len(sectionTitle)

            self._minitel.inverse(True)
            self._minitel._print(elem_index)
            self._minitel.inverse(False)

            self._minitel._print(elem)
            curPos = self._minitel.curpos()
            self._minitel._del(*curPos)
            self._minitel._print("\n")

        self._minitel.flash()
        self.handle_input()

    def handle_input(self):
        current_input = self._minitel.get()
        selection = 0
        while current_input != Teletel.ENVOI.value:
            current_input = self._minitel.input(20, 38, 2)
            print(current_input)

    def _draw_footer(self):
        pass


