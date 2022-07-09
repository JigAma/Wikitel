from pynitel.pynitel import Pynitel
import serial

from abc import ABC, abstractmethod


class ViewController(ABC):
    _minitel = None

    def __init__(self, baudrate, port):

        if not ViewController._minitel:
            ViewController._minitel = Pynitel(serial.Serial(port, baudrate, parity=serial.PARITY_EVEN, bytesize=7, timeout=2))

    def draw(self):
        self._minitel.home()

    @staticmethod
    def calculate_nb_of_lines(text):
        """
        Calculate the number of lines taken by a text on the minitel screen

        :param str text:
        :return: The number of lines on which text will be printed
        :rtype: int
        """

        nb_of_lines = len(text)//Pynitel.COL_SIZE
        nb_of_lines += text.count('\n')
        return nb_of_lines
