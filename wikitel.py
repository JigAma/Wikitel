from pynitel.pynitel import Pynitel
import wikipedia
import serial

wikipedia.set_lang("fr")
class Wikitel:
    
    def __init__(self, pynitel=Pynitel(serial.Serial('/dev/ttyUSB0', 1200, parity=serial.PARITY_EVEN, bytesize=7, timeout=2))):
        self.minitel = pynitel
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

    def __buttonIndication(self, text, button_name, line=0, col=0):
        """

        :param string text:
        :param string button_name:
        :param int line:
        :param int col:
        """
        if line and col:
            self.minitel.pos(line, col)

        self.minitel._print(text + " → ")
        self.minitel.inverse(True)
        self.minitel._print(button_name.upper())
        self.minitel.inverse(False)

    def showPage(self, page=wikipedia.page(title="SNCF", auto_suggest=False, preload=True)):
        self.currentPage = page
        self.summary()

    def summary(self):
        self.__header("Résumé")
        self.minitel._print(wikipedia.summary(self.currentPage.title))

        self.__buttonIndication("Défiler vers le bas", "suite", self.minitel.LINE_SIZE-2, 1)
        self.__buttonIndication("Sommaire", "sommaire", self.minitel.LINE_SIZE-1, 1)
        while True:
            key = self.minitel.getKey()
            if key == self.minitel.SOMMAIRE:
                self.tableOfContent()
                break
            elif key == self.minitel.SUITE:
                print("NON IMPLEMENTE")
                self.minitel.message(0, 1, 5, "NON IMPLEMENTE", True)

    def tableOfContent(self):
        self.__header("Sommaire\n")
        for i, section in enumerate(self.currentPage.sections):
            self.minitel.inverse(True)
            self.minitel._print("{})".format(i+1))
            self.minitel.inverse(False)
            self.minitel._print(section + "\n")
        



# minitel.waitzones(0)
# result = self.minitel.zones[0]['texte']
# print(result)


if __name__ == "__main__":

    w = Wikitel()
    w.showPage()

