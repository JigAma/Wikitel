from pynitel.pynitel import Pynitel
import wikipedia
from views.HomeViewController import *
import platform

import test_variable
from views.PageViewController import PageViewController

wikipedia.set_lang("fr")

class Wikitel:
    
    def __init__(self):
        
        self.PORT = "COM3"
        if platform.system() == "Linux":
            self.PORT = '/dev/ttyUSB0'

        self.BAUDRATE = 4800
        self.current_viewcontroller = HomeViewController(self.BAUDRATE, self.PORT)
        if self.BAUDRATE == 4800:
            print("/!\\ Appuyez sur Fct + P -> " + str(self.BAUDRATE//1000))

        self.FOOTER_SIZE = 0
        self.current_viewcontroller.draw()
        search_input = self.current_viewcontroller.get_searchtext_input()

        if isinstance(search_input, int):
            # Gérer touches Télétel (Guide, Sommaire, Suite)
            pass
        else:
            self.showPage()


    def __header(self, section_name):
        """
        print a page header on self.minitel

        :param string section_name:
        """
        # Title
        self.minitel.home()
        self.minitel._print(self.currentPage.title + "\n")
        self.minitel.plot("_", 40)
        self.minitel.inverse(True)
        self.minitel.scale(3)
        self.minitel._print(section_name)
        self.minitel.inverse(False)
        self.minitel.scale(0)

    def __footer(self, buttonsText, buttons):
        """
        Print un footer sur la page

        :param tuple[str] buttonsText: texte associé au bouton
        :param tuple[int] buttons: constante du bouton déclaré dans Pynitel
        """
        self.FOOTER_SIZE = len(buttons)

        BUTTONS = ["ENVOI", "RETOUR", "REPETITION", "GUIDE", "ANNULATION", "SOMMAIRE", "CORRECTION", "SUITE", "CONNEXION FIN"]
        if len(buttonsText) != len(buttons):
            raise ValueError("buttonsText et buttons doivent avoir la même taille")
        self.minitel.pos(self.minitel.LINE_SIZE-len(buttons))
        self.minitel.plot("_", 40)

        for (buttonText, button) in zip(buttonsText, buttons):
            self.minitel._print(buttonText + " → ")
            self.minitel.inverse(True)
            self.minitel._print(BUTTONS[button-1] + "\n")
            self.minitel.inverse(False)

    def __paragraphSize(self, startPos, footerSize=0):
        self.minitel.cursor(True)
        paragraphSize = self.minitel.COL_SIZE - startPos[1] + 1
        paragraphSize += (self.minitel.LINE_SIZE - (startPos[0]) - footerSize) * self.minitel.COL_SIZE

        return paragraphSize

    def __getPages(self, text, maxPageSize=Pynitel.COL_SIZE*Pynitel.LINE_SIZE):
        """
        :param str text: text to split in pages
        :param int maxPageSize: maximum number of characters in a page, default value is the maximum number of characters displayable on the Minitel screen
        :return: a list of index of all pages
        """
        #maxPageSize-=1
        nb_of_pages = len(text) // maxPageSize
        pages = [0] * nb_of_pages

        i = 0
        for char_i, char in enumerate(text):
            if char_i >= pages[i]:
                i += 1

                if i >= len(pages):
                    pages.append(pages[-1] + maxPageSize)
                pages[i] = pages[i - 1] + maxPageSize

            if char == '\n':
                char_pos = char_i % Pynitel.COL_SIZE
                pages[i] -= (Pynitel.COL_SIZE - char_pos)

        # DEBUG TEST
        for i in range(1, len(pages)):
            if pages[i] - pages[i-1] > maxPageSize:
                print("ERREUR: pages[{}] > {} ({})".format(i, maxPageSize, pages[i] - pages[i-1]))
        return pages

    def __printParagraph(self, text, startCurPos, endIdx, startIdx=0):

        self.minitel.pos(startCurPos[0], startCurPos[1])

        self.minitel._print(text[startIdx:endIdx])
        end_pos = self.minitel.curpos()
        self.minitel.canblock(end_pos[0], self.minitel.LINE_SIZE-self.FOOTER_SIZE, end_pos[1])
        self.minitel.pos(startCurPos[0], startCurPos[1])  # reset curpos at original position

    def showPage(self, page=wikipedia.page(title="Napoléon Ier", auto_suggest=False, preload=True)):
        """
        Display Wikipedia Page on self.minitel

        :param wikipedia.WikipediaPage page: page to display
        """
        self.currentPage = page
        self.current_viewcontroller = PageViewController(self.BAUDRATE, self.PORT)

        self.current_viewcontroller.set_page_title(page.title)
        self.current_viewcontroller.set_page_section_name("Résumé")

        page_buttons = (Teletel.SUITE, Teletel.SOMMAIRE)
        buttons_text = ("Défiler vers le bas", "Sommaire")
        self.current_viewcontroller.set_page_buttons(page_buttons, buttons_text)
        self.current_viewcontroller.draw()

        self.current_viewcontroller.print_content() #TODO

    def summary(self):
        self.__header("Résumé")
        curPos = self.minitel.curpos()
        self.__footer(("Défiler vers le bas", "Sommaire"), (self.minitel.SUITE, self.minitel.SOMMAIRE))
        self.minitel.pos(0, 1)
        self.minitel.flash(True)
        self.minitel._print("Chargement...")
        self.minitel.flash(False)
        summary = wikipedia.summary(self.currentPage.title)
        paragrapheLen = self.__paragraphSize(curPos, 2)
        self.__printParagraph(summary, curPos, paragrapheLen)

        print("texte: " + str(len(summary)) + " caractères")     # TODO: DEBUG
        self.minitel._del(0, 1)
        paragrapheLen = self.__paragraphSize(curPos, 3)
        pagesindex = self.__getPages(summary, paragrapheLen)
        summary = summary.replace('\n', '\\') # TODO: DEBUG
        i = -1
        print(pagesindex)
        key = self.minitel.SUITE
        while True:

            if key == self.minitel.SOMMAIRE:
                self.tableOfContent()
            elif key == self.minitel.SUITE:
                if pagesindex[i+1] < len(summary):    # Check out of bounds
                    i += 1
                    self.__printParagraph(summary, curPos, pagesindex[i+1], pagesindex[i])

                else:
                    self.minitel.message(0, 1, 1, "Fin de la page", True)
            elif key == self.minitel.RETOUR:
                if i > 0:     # Check out of bounds
                    i -= 1
                    self.__printParagraph(summary, curPos, pagesindex[i+1], pagesindex[i])
                else:
                    self.minitel.message(0, 1, 1, "Début de la page", True)
            elif key == self.minitel.REPETITION:
                self.__header("Résumé")
                self.__footer(("Défiler vers le bas", "Sommaire"), (self.minitel.SUITE, self.minitel.SOMMAIRE))
                self.__printParagraph(summary, curPos, pagesindex[i+1], pagesindex[i])
            else:
                self.minitel.message(0, 1, 1, "Pas implémenté", True)

            key = self.minitel.getKey()

    def tableOfContent(self):
        self.__header("Sommaire\n")
        startCurPos = self.minitel.curpos()
        paragraphLen = self.__paragraphSize(startCurPos, 0)
        self.minitel.cursor(True)
        totalPrinted = 0
        for i, sectionTitle in enumerate(self.currentPage.sections):
            toPrint = "{})".format(i + 1)
            printedThisLoop = len(toPrint) + len(sectionTitle)
            printedThisLoop += self.minitel.COL_SIZE - (len(toPrint) + len(sectionTitle) % self.minitel.COL_SIZE)  # \n
            totalPrinted += printedThisLoop

            if totalPrinted > paragraphLen:
                self.minitel.canblock(self.minitel.curpos()[0], self.minitel.LINE_SIZE, 1)
                self.minitel.pos(1, 1)
                while True:
                    key = self.minitel.getKey()
                    if key == self.minitel.SUITE:
                        totalPrinted = printedThisLoop
                        self.minitel.pos(startCurPos[0], startCurPos[1])
                        break

            self.minitel.inverse(True)
            self.minitel._print(toPrint)
            self.minitel.inverse(False)

            self.minitel._print(sectionTitle)
            curPos = self.minitel.curpos()
            self.minitel._del(curPos[0], curPos[1])
            self.minitel._print("\n")


if __name__ == "__main__":

    w = Wikitel()
    w.showPage()
