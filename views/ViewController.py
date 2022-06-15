from pynitel.pynitel import Pynitel
import serial

from abc import ABC, abstractmethod


class ViewController(ABC):

    def __init__(self, baudrate, port):
        if not ViewController._minitel:
            ViewController._minitel = Pynitel(serial.Serial(port, baudrate, parity=serial.PARITY_EVEN, bytesize=7, timeout=2))

    def draw(self):
        self._minitel.home()
