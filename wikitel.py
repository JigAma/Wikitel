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

    def __paragraphSize(self, startPos, footerSize=0):
        self.minitel.pos(startPos[0], startPos[1])

        paragraphSize = self.minitel.COL_SIZE - startPos[1]
        paragraphSize += (self.minitel.LINE_SIZE - (startPos[0] + 1) - footerSize) * self.minitel.COL_SIZE
        print(paragraphSize)

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
        self.minitel.pos(self.minitel.LINE_SIZE - 2)
        self.minitel.plot("_", 40)
        self.__buttonIndication("Défiler vers le bas", "suite", self.minitel.LINE_SIZE - 1, 1)
        self.__buttonIndication("Sommaire", "sommaire", self.minitel.LINE_SIZE, 1)

        #summary = wikipedia.summary(self.currentPage.title)
        summary = "Napoléon Bonaparte, né le 15 août 1769 à Ajaccio et mort le 5 mai 1821 sur l'île Sainte-Hélène, est un militaire et homme d'État français, premier empereur des Français du 18 mai 1804 au 6 avril 1814 et du 20 mars au 22 juin 1815, sous le nom de Napoléon Ier Second enfant de Charles Bonaparte et Letizia Ramolino, Napoléon Bonaparte devient en 1793 général dans les armées de la Première République française, née de la Révolution, où il est notamment commandant en chef de l'armée d'Italie puis de l'armée d'Orient. Arrivé au pouvoir en 1799 par le coup d'État du 18 Brumaire, il est Premier consul — consul à vie à partir du 2 août 1802 — jusqu'au 18 mai 1804, date à laquelle l'Empire est proclamé par un sénatus-consulte suivi d'un plébiscite. Il est sacré empereur, en la cathédrale Notre-Dame de Paris, le 2 décembre 1804, par le pape Pie VII, en même temps que son épouse Joséphine de Beauharnais.  En tant que général en chef et chef d'État, Napoléon tente de briser les coalitions montées et financées par le royaume de Grande-Bretagne et qui rassemblent, à partir de 1792, les monarchies européennes contre la France et son régime né de la Révolution. Il conduit les armées françaises d'Italie au Nil et d'Autriche à la Prusse et à la Pologne : les nombreuses et brillantes victoires de Bonaparte (Arcole, Rivoli, Pyramides, Marengo, Austerlitz, Iéna, Friedland), dans des campagnes militaires rapides, disloquent les quatre premières coalitions. Les paix successives, qui mettent un terme à chacune de ces coalitions, renforcent la France et donnent à Napoléon un degré de puissance jusqu'alors rarement égalé en Europe, lors de la paix de Tilsit (1807).Napoléon réforme durablement l'État, en restaurant son autorité et sa primauté. La France connaît d'importances réformes, qui font de Napoléon l'un des pères fondateurs des institutions contemporaines françaises. En ce sens, les codifications napoléoniennes, dont le code civil de 1804, permettent de renforcer les libertés individuelles ou l'égalité des citoyens devant la loi, en opérant une synthèse par la garantie de certains acquis révolutionnaires et la reprise de principes traditionnels issus de l'Ancien Régime. L'administration française est réorganisée, avec la création des préfets dans les départements. De même, une nouvelle monnaie émerge, le franc, tandis qu'est instaurée la Banque de France. Le Conseil d'État est également créé, tout comme les lycées. Napoléon tente également de renforcer l'empire colonial français de l'Ancien Régime en outre-mer. Alors que la Révolution haïtienne tourne à la sécession dans cette colonie, Napoléon rétablit l'esclavage en 1802, rétablissement qu’il souhaite provisoire, notamment pour empêcher l’indépendance proclamée de l'île par le général Toussaint-Louverture. Toujours pour des raisons politiques, Napoléon revend paradoxalement la Louisiane aux Etats-Unis, en 1803. Il perdra cependant la plupart des colonies qui l’intéressaient face aux anglais, et perdra Saint-Domingue à la suite de l'échec de l'expédition militaire préalable (1802-1803), visant à combattre les indépendantistes. Napoléon porte le territoire français à son extension maximale en Europe, avec 134 départements en 1812, transformant Rome, Hambourg, Barcelone ou Amsterdam en chefs-lieux de départements français. Il est aussi président de la République italienne de 1802 à 1805, roi d'Italie de 1805 à 1814, médiateur de la Confédération suisse de 1803 à 1813 et protecteur de la confédération du Rhin de 1806 à 1813. Ses victoires lui permettent d'annexer à la France de vastes territoires et de gouverner la majeure partie de l'Europe continentale en plaçant les membres de sa famille sur les trônes de plusieurs royaumes : Joseph à Naples puis en Espagne, Louis en Hollande, Jérôme en Westphalie et son beau-frère Joachim Murat à Naples. Il crée également un duché de Varsovie, sans restaurer formellement l'indépendance polonaise, et soumet temporairement à son influence des puissances vaincues telles que le royaume de Prusse et l'empire d'Autriche.Objet dès son vivant d'une légende dorée comme d'une légende noire, il doit sa très grande notoriété à son habileté militaire, récompensée par de nombreuses victoires, et à sa trajectoire politique étonnante, mais aussi à son régime despotique et très centralisé ainsi qu'à son ambition, qui se traduit par des guerres meurtrières (au Portugal, en Espagne et en Russie) avec des millions de morts et blessés, militaires et civils pour l'ensemble de l'Europe. Il est considéré comme l'un des plus grands commandants de l'histoire, et ses guerres et campagnes sont étudiées dans les écoles militaires du monde entier.Alors qu'ils financent des coalitions de plus en plus générales, les Alliés finissent par remporter des succès décisifs en Espagne (bataille de Vitoria) et en Allemagne (bataille de Leipzig) en 1813. L'intransigeance de Napoléon devant ces revers lui fait perdre le soutien de pans entiers de la nation française, tandis que ses anciens alliés ou vassaux se retournent contre lui. Amené à abdiquer en 1814 après la prise de Paris, capitale de l'Empire français, et à se retirer à l'île d'Elbe, il tente de reprendre le pouvoir en France, lors de l'épisode des Cent-Jours en 1815. Capable de reconquérir la France et d'y rétablir le régime impérial sans coup férir, il amène pourtant, à la suite de diverses trahisons et dissensions de ses maréchaux, le pays dans une impasse avec la lourde défaite de Waterloo, qui met fin à l'Empire napoléonien et assure la restauration de la dynastie des Bourbons. Sa mort en exil, à Sainte-Hélène, sous la garde des Anglais, fait l'objet de nombreuses controverses.Une tradition romantique fait de Napoléon l'archétype du « grand homme » appelé à bouleverser le monde. C'est ainsi que le comte de Las Cases, auteur du Mémorial de Sainte-Hélène, tente de présenter Napoléon au Parlement britannique dans une pétition rédigée en 1818. Élie Faure, dans son ouvrage Napoléon, qui a inspiré Abel Gance, le compare à un « prophète des temps modernes ». D'autres auteurs, tel Victor Hugo, font du vaincu de Sainte-Hélène le « Prométhée moderne ». L'ombre de « Napoléon le Grand » plane sur de nombreux ouvrages de Balzac, Stendhal, Musset, mais aussi de Dostoïevski, de Tolstoï et de bien d'autres encore. Par ailleurs, un courant politique français émerge au XIXe siècle, le bonapartisme, se réclamant de l'action et du mode de gouvernement de Napoléon."
        paragrapheLen = self.__paragraphSize(curPos, 2)
        self.__printParagraph(summary, curPos, paragrapheLen)

        i = 1
        while True:
            key = None
            key = self.minitel.getKey()


            if key == self.minitel.SOMMAIRE:
                self.tableOfContent()
                break
            elif key == self.minitel.SUITE:
                self.__printParagraph(summary, curPos, paragrapheLen, i*paragrapheLen)
                i += 1

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

