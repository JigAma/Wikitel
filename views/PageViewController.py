from Teletel import Teletel
from views.ViewController import *


class PageViewController(ViewController):

    def __init__(self, baudrate, port):
        super().__init__(baudrate, port)

        self.title = self.section = ""
        self.page_buttons = self.page_buttons_text = []
        self.top_of_page = ()

    def draw(self):
        super().draw()
        self._draw_header()
        self._draw_footer()

    def _draw_header(self):
        """ print a page header on minitel """

        # Page Title
        self._minitel._print(self.title + "\n")
        self._minitel.plot("_", 40)

        # section name
        self._minitel.inverse(True)
        self._minitel.scale(3)
        self._minitel._print(self.section)
        self._minitel.inverse(False)
        self._minitel.scale(0)

        self.top_of_page = self._minitel.curpos()

    def set_page_title(self, title: str):
        """
        Set the page title.

        Length should be 40 characters at maximum,
        else the page section name will be printed on multiple lines.

        :param title: the title of the page to print
        """
        self.title = str(title)

    def set_page_section_name(self, section_name: str):
        """
        Set the page section name.

        Length should be 20 characters at maximum,
        else the page section name will be printed on multiple lines.

        :param section_name: the name of the section to print
        """
        self.section = str(section_name)

    def _draw_footer(self):
        """
        Draw page footer
        """
        buttons_number = len(self.page_buttons)
        if buttons_number > 0:
            self._minitel.pos(self._minitel.LINE_SIZE-buttons_number)
            self._minitel.plot("_", 40)

            for (button, buttonText) in zip(self.page_buttons, self.page_buttons_text):
                self._minitel._print(buttonText + " → ")
                self._minitel.inverse(True)
                self._minitel._print(button.name + "\n")
                self._minitel.inverse(False)

    def set_page_buttons(self, teletel_buttons, buttons_text):
        """
        Set the Teletel buttons usable on that page

        :param tuple[Teletel] teletel_buttons: List of Teletel buttons usable
        :param tuple[str] buttons_text: text associated with each button. Should be short
        """
        if len(teletel_buttons) != len(buttons_text):
            raise ValueError("There must be a text associated with each button.")
        else:
            self.page_buttons = teletel_buttons
            self.page_buttons_text = buttons_text

    def print_content(self, text):
        self._minitel.pos(*self.top_of_page)
        self._minitel._print(text)
