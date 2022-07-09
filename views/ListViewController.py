
from Teletel import Teletel
from views.ViewController import *


class ListViewController(ViewController):

    def __init__(self, baudrate, port):
        super().__init__(baudrate, port)

        self.top_of_page = ()  # x,y position of top of page
        self.displayed_list = []  # current displayed list

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
        """
        Handle the selection of an item on the list by the user

        :return: the selected item
        :rtype: str
        """
        ENVOI_BYTE = b'\x13'
        selected_elem = self.displayed_list[0]
        i = 1
        do_error_happened = False
        while True:
            data = self._minitel._if()

            if data:
                try:
                    if data == ENVOI_BYTE:
                        return self.displayed_list[i - 1]

                    if not do_error_happened:
                        previous_i = i
                    do_error_happened = False
                    i = int(data)
                    if 0 > i-1 or i-1 > len(self.displayed_list):   # Check out of bounds
                        raise IndexError

                    # Redraw previously selected element
                    self._minitel.pos(self.top_of_page[0] + previous_i - 1)
                    self._print_line(previous_i, selected_elem, False)

                    selected_elem = self.displayed_list[i - 1]

                    # Draw current selected element with emphasis
                    self._minitel.pos(self.top_of_page[0] + i - 1)
                    self._print_line(i, selected_elem, True)

                    self._minitel.pos(self._minitel.LINE_SIZE, self._minitel.COL_SIZE-1)    # pos cursor at bottom right because of local echo

                except ValueError:
                    self._minitel.message(0, 1, 1, "ERREUR: Utilisez le pavé numérique", True)
                    do_error_happened = True
                except IndexError:
                    self._minitel.message(0, 1, 1, "ERREUR: Index invalide.", True)
                    do_error_happened = True

    def _draw_footer(self):
        pass
