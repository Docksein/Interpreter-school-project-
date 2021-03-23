import sys
from pathlib import Path


class InputStream:
    """
    Usnadňuje práci a manipulaci se vstupním souborem

    Při lexikální analýze je třeba pracovat se efektivně pohybovat ve zdrojovém kódu. Právě k
    tomu slouží třída InputStream, která obaluje vstupní soubor a usnadňuje nám práci s ním.
    """
    
    @staticmethod
    def from_file(file_name: str):
        """
        Vytvoří instanci vstupního streamu pro zadaný soubor
        """
        return InputStream(Path(file_name).read_text())

    def __init__(self, buffer: str):
        """
        Konstruktor

        Konstruktor je volán při vytvoření objektu. Slouží zejména k nastavení všech důležitých
        atributů objektu, jako je například aktuální pozice v bufferu, případně buffer samotný.

        :param buffer: Buffer obsahující celý zdrojový kód.
        :return: self
        """
        self.__buffer = buffer
        self.__pos = 0
        self.__col = 0
        self.__line = 1

    def peek(self) -> str:
        """
        Vrátí aktuálně čtený znak

        Vrácený znak zůstává součástí vstupu, tedy se v bufferu nijak neposunujeme. V případě
        bezprostředně opakovaného volání funkce peek() je vrácen ten samý znak.

        :return: Znak na aktuální pozici ve zdrojovém kódu.
        """
        return self.__buffer[self.__pos]

    def next(self) -> str:
        """
        Vrátí aktuálně čtený znak a přesune se v bufferu na znak následující

        V případě, že jsme došli na konec vstupu, tak není chování funkce definováno a
        pravděpodobně skončí chybou.

        :return: Znak na aktuální pozici ve zdrojovém kódu.
        """
        char = self.peek()
        self.__pos += 1

        if char == '>' or char == '<' or char == '!' or char == '=':
            nextChar = self.peek()
            if nextChar == '=':
                char = char + nextChar
                self.__pos += 1

        if char == '\n':
            self.__line += 1
            self.__col = 0
        else:
            self.__col += 1

        return char

    def is_eof(self) -> bool:
        """
        Testuje, zda se již nacházíme na konci zdrojového souboru

        :return: True v případě, že jsme došli na konec vstupu, False jinak.
        """
        return self.__pos >= len(self.__buffer)

    def raise_error(self, msg: str) -> None:
        """
        Vypíše na chybový výstup detail chyby, ke které došlo během lexikální analýzy.

        Součástí chybové hlášky jsou i detaily toho, ve které části zdrojového kódu se právě
        nacházíme.

        :param msg: Detailní chybová zpráva zobrazená uživateli.
        :return: None
        """
        print("Error occurred [l:{:d}, c:{:d}]: {:s}".format(self.__line, self.__col, msg),
              file=sys.stderr)
        exit()
