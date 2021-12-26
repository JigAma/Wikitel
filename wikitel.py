from pynitel.pynitel import Pynitel
import wikipedia
import serial

wikipedia.set_lang("fr")
class Wikitel:
    
    def __init__(self, pynitel=Pynitel(serial.Serial('/dev/ttyUSB0', 4800, parity=serial.PARITY_EVEN, bytesize=7, timeout=2))):
        self.minitel = pynitel
        if self.minitel.conn.baudrate == 4800:
            print("/!\\ Appuyez sur Fct + P -> 4 ")
        self.minitel.home()

        self.currentPage = None

        self.minitel.xdraw('ecrans/home.vdt')
        self.minitel.resetzones()
        self.minitel.zone(13, 15, 10, '', self.minitel.BLANC)

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
        BUTTONS = ["ENVOI", "RETOUR", "REPETITION", "GUIDE", "ANNULATION", "SOMMAIRE", "CORRECTION", "SUITE", "CONNEXION FIN"]
        if len(buttonsText) != len(buttons):
            raise ValueError("buttonsText et buttons doit être de la même taille")
        nbOfButtons = len(buttons)
        self.minitel.pos(self.minitel.LINE_SIZE-nbOfButtons)
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

    def __printParagraph(self, text, startCurPos, paragraphSize, startIdx=0):

        self.minitel.pos(startCurPos[0], startCurPos[1])
        self.minitel._print(text[startIdx:startIdx + paragraphSize])
        self.minitel.pos(startCurPos[0], startCurPos[1])  # reset curpos at original position

    def showPage(self, page=wikipedia.page(title="Napoléon Ier", auto_suggest=False, preload=True)):
        """
        Display Wikipedia Page on self.minitel

        :param wikipedia.WikipediaPage page: page to display
        """
        self.currentPage = page
        self.summary()

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

        i = 0
        maxi = len(summary) // paragrapheLen
        while True:
            key = self.minitel.getKey()

            if key == self.minitel.SOMMAIRE:
                self.tableOfContent()
                break
            elif key == self.minitel.SUITE:
                if i < maxi:
                    i += 1
                    self.__printParagraph(summary, curPos, paragrapheLen, i*paragrapheLen)
                else:
                    self.minitel.message(0, 1, 1, "Fin de la page", True)
            elif key == self.minitel.RETOUR:
                if i > 0:
                    i -= 1
                    self.__printParagraph(summary, curPos, paragrapheLen, i * paragrapheLen)
                else:
                    self.minitel.message(0, 1, 1, "Début de la page", True)
            elif key == self.minitel.REPETITION:
                self.__header("Résumé")
                self.__printParagraph(summary, curPos, paragrapheLen, i * paragrapheLen)
                self.__footer(("Défiler vers le bas", "Sommaire"), (self.minitel.SUITE, self.minitel.SOMMAIRE))
            else:
                self.minitel.message(0, 1, 1, "Pas implémenté", True)

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



# minitel.waitzones(0)
# result = self.minitel.zones[0]['texte']
# print(result)


if __name__ == "__main__":

    w = Wikitel()
    w.showPage()

