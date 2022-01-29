########################################################################################################################
# Module importieren
########################################################################################################################

from random import randint
import qdarkstyle
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
import sys
import GraphicalDisplay
import GraphicalDiagram
import re
import os
import ast


########################################################################################################################
# Klasse: Main definieren
########################################################################################################################

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('Window.ui', self)
        sshFile = "style.qss"
        with open(sshFile, "r") as fh:
           self.setStyleSheet(fh.read()) # Dunkles Stylesheet laden
        self.show()
        self.setWindowTitle("Van Der Wearden Numbers")

        ########################################################################################################################
        # GUI elemente als Attribute laden
        ########################################################################################################################

        self.InfoChooser = self.findChild(QtWidgets.QComboBox, "InfoChooser")
        self.ModeChooser = self.findChild(QtWidgets.QComboBox, "ModeChooser")
        self.GoalChooser = self.findChild(QtWidgets.QSpinBox, "GoalChooser")
        self.ColorChooser = self.findChild(QtWidgets.QSpinBox, "ColorChooser")
        self.PatternChooser = self.findChild(QtWidgets.QSpinBox, "PatternChooser")
        self.DisplayButton = self.findChild(QtWidgets.QPushButton, "DisplayButton")
        self.DisplayButton.pressed.connect(self.display)
        self.DiagramButton = self.findChild(QtWidgets.QPushButton, "DiagramButton")
        self.DiagramButton.pressed.connect(self.diagram)
        self.SortButton = self.findChild(QtWidgets.QPushButton, "SortButton")
        self.SortButton.pressed.connect(self.sort)
        self.SortoutButton = self.findChild(QtWidgets.QPushButton, "SortoutButton")
        self.SortoutButton.pressed.connect(self.sortout)
        self.Start = self.findChild(QtWidgets.QPushButton, "Start_2")
        self.Start.pressed.connect(self.start)
        self.Pause = self.findChild(QtWidgets.QPushButton, "Pause_2")
        self.Pause.pressed.connect(self.pause)
        self.Stop = self.findChild(QtWidgets.QPushButton, "Stop_2")
        self.Stop.pressed.connect(self.stop)
        self.ActionStart = self.findChild(QtWidgets.QAction, "actionStart")
        self.ActionStart.triggered.connect(self.start)
        self.ActionPause = self.findChild(QtWidgets.QAction, "actionPause")
        self.ActionPause.triggered.connect(self.pause)
        self.ActionStop = self.findChild(QtWidgets.QAction, "actionStop")
        self.ActionStop.triggered.connect(self.stop)
        self.ActionQuit = self.findChild(QtWidgets.QAction, "actionQuit")
        self.ActionQuit.triggered.connect(self.close)
        self.ActionClear = self.findChild(QtWidgets.QAction, "actionClear_console")
        self.ActionClear.triggered.connect(self.clear)
        self.ActionSave = self.findChild(QtWidgets.QAction, "actionSave_as")
        self.ActionSave.triggered.connect(self.saveFileDialog)
        self.ActionOpen = self.findChild(QtWidgets.QAction, "actionOpen")
        self.ActionOpen.triggered.connect(self.openFileDialog)
        self.TextBrowser = self.findChild(QtWidgets.QTextBrowser, "TextBrowser_3")
        self.info = self.findChild(QtWidgets.QTextBrowser, "info")
        self.nextgoal = self.GoalChooser.value()
        self.nextmode = "EinDurchlauf"
        self.nextmode = "Rekord"

        self.updater = QTimer()
        self.updater.timeout.connect(self.OnUpdate)
        self.updater.start(1)
        self.status = False

        ########################################################################################################################
        # Grund variablen definieren
        ########################################################################################################################

        self.AvailableColors = ["R", "G", "B", "Y", "A", "C", "O", "W", "L", "P"]
        self.colors = self.AvailableColors[0:self.ColorChooser.value()]
        self.patternlenth = self.PatternChooser.value()
        self.pattern = None
        self.attempts = 0
        self.done = False
        self.Types = {}
        self.chainlist = []
        for color in self.colors:
            self.Types[color] = []
        self.LastElement = 0
        self.attempts += 1
        self.record = 0
        self.inputchain = []
        self.alive = True

    ########################################################################################################################
    # Funktion zum Speichern von Dateien definieren
    ########################################################################################################################

    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, "Aktuelle liste speichern", "", "Text Files (*.vwn);;All Files (*)", options=options)
        if fileName:
            selectedExt = re.search('\((.+?)\)',fileFilter).group(1).replace('*','')
            if not os.path.splitext(fileName)[1]:
                fileName = fileName + selectedExt
            newfile = open(fileName, "w")
            newfile.write(str(self.chainlist))
            newfile.write("\n" + str(len(self.chainlist)))
            newfile.write("\n" + str(self.nextgoal))
            newfile.write("\n" + str(self.colors))
            newfile.write("\n" + str(self.patternlenth))
            newfile.write("\n" + self.info.toPlainText())
            newfile.write("\n" + self.TextBrowser.toPlainText())
            newfile.close()

    ########################################################################################################################
    # Funktion zum Öffnen von Dateien definieren
    ########################################################################################################################

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.DontConfirmOverwrite
        fileName, fileFilter = QtWidgets.QFileDialog.getSaveFileName(self, "eine Datei öffnen", "", "Text Files (*.vwn);;All Files (*)", options=options)
        if fileName:
            file = open(fileName, "r")
            text = file.readlines()
            self.chainlist = ast.literal_eval(text[0])
            lineamount = int(text[1])
            self.nextgoal = int(text[2])
            self.colors = ast.literal_eval(text[3])
            self.patternlenth = int(text[4])
            self.GoalChooser.setValue(self.nextgoal)
            self.ColorChooser.setValue(len(self.colors))
            self.PatternChooser.setValue(self.patternlenth)
            list1 = text[5: 5 + lineamount]
            text1 = ""
            for string in list1:
                text1 = text1 + string
            list2 = text[5 + lineamount:]
            text2 = ""
            for string in list2:
                text2 = text2 + string
            self.info.setText(text1)
            self.TextBrowser.setText(text2)
            file.close()
            self.DisplayButton.setEnabled(True)
            self.DiagramButton.setEnabled(True)
            self.SortButton.setEnabled(True)
            self.SortoutButton.setEnabled(True)

    ########################################################################################################################
    # Fenster zur grafischen Darstellung öffnen
    ########################################################################################################################

    def display(self):
        if self.chainlist:
            GraphicalDisplay.open(self.chainlist)

    ########################################################################################################################
    # Fenster fürs Wegdiagramm öffnen
    ########################################################################################################################

    def diagram(self):
        if self.chainlist:
            GraphicalDiagram.open(self.chainlist, self.colors)

    ########################################################################################################################
    # Ketten nach Farben sortieren
    ########################################################################################################################

    def sort(self):
        self.chainlist.sort()
        self.info.clear()
        for chain in self.chainlist:
            self.info.append(str(chain))

    ########################################################################################################################
    # Doppelte Ketten aussortieren
    ########################################################################################################################

    def sortout(self):
        deletelist = []
        for originalind in range(0, len(self.chainlist)):
            if originalind < len(self.chainlist):
                originalchain = self.chainlist[originalind][:-1]
                newind = 0
                for newchain in self.chainlist:
                    if not originalind == newind:
                        newchain2 = newchain[:-1]
                        for i in range(len(self.colors)):
                            if originalchain == newchain2:
                                self.TextBrowser.append("##########################################################################")
                                self.TextBrowser.append(str(self.chainlist[originalind]) + "<-- Originalkette")
                                self.TextBrowser.append(str(newchain) + "<-- gefundene identische Kette")
                                deletelist.append(newchain)
                                del self.chainlist[newind]
                                newind -= 1
                                originalind -= 1
                            newchainbackup = newchain2[:]
                            newchain2 = []
                            for element in newchainbackup:
                                nextcolor = self.colors.index(element) + 1
                                if nextcolor < len(self.colors):
                                    newchain2.append(self.colors[nextcolor])
                                else:
                                    newchain2.append(self.colors[0])
                    newind += 1
            else:
                break
        self.info.clear()
        for chain in self.chainlist:
            self.info.append(str(chain))
        self.TextBrowser.append("Es wurden " + str(len(deletelist)) + " Elemente gelöscht.")

    ########################################################################################################################
    # Info-Konsole leeren
    ########################################################################################################################

    def clear(self):
        self.TextBrowser.clear()

    ########################################################################################################################
    # Grundvariablen für Start zurücksetzen
    ########################################################################################################################

    def start(self):
        self.chainlist = []
        self.info.clear()
        self.colors = self.AvailableColors[0:self.ColorChooser.value()]
        self.patternlenth = self.PatternChooser.value()
        self.status = True
        self.done = False
        self.record = 0
        self.Pause.setEnabled(True)
        self.Stop.setEnabled(True)
        self.DisplayButton.setEnabled(False)
        self.DiagramButton.setEnabled(False)
        self.SortButton.setEnabled(False)
        self.SortoutButton.setEnabled(False)
        self.nextmode = "EinDurchlauf"
        self.nextgoal = 27
        if self.ModeChooser.currentIndex() == 0:
            self.nextmode = "EinDurchlauf"
        elif self.ModeChooser.currentIndex() == 1:
            self.nextgoal = self.GoalChooser.value()
            self.nextmode = "SoOftBis"
        elif self.ModeChooser.currentIndex() == 2:
            self.nextgoal = self.GoalChooser.value()
            self.nextmode = "EndlosModus"
        if self.InfoChooser.currentIndex() == 0:
            self.infomode = "Rekord"
        if self.InfoChooser.currentIndex() == 1:
            self.infomode = "Liste"

        self.attempts = 0
        self.cleartimer = 0
        self.done = False

    ########################################################################################################################
    # Programm pausieren
    ########################################################################################################################

    def pause(self):
        self.status = not self.status

    ########################################################################################################################
    # Durchlauf stoppen
    ########################################################################################################################

    def stop(self):
        self.status = False
        self.done = True
        self.Stop.setEnabled(False)
        self.Pause.setEnabled(False)
        self.Start.setEnabled(True)

    ########################################################################################################################
    # Bei jeder neuen Programmiteration
    ########################################################################################################################

    def OnUpdate(self):
        if self.status:
            self.Start.setEnabled(False)
            if not self.done:
                for color in self.colors:
                    self.Types[color] = []
                self.LastElement = 0
                self.attempts += 1
                self.cleartimer += 1
                self.inputchain = []
                self.alive = True
                self.Algorithm(self.nextmode, self.nextgoal)

    ########################################################################################################################
    # Muster-Erkennungsalgorithmus
    ########################################################################################################################

    def FindPattern(self):
        color = self.inputchain[self.LastElement]
        for second in reversed(self.Types[color]):
            distance = self.LastElement - second
            infochain = [self.LastElement, second]
            nextpattern = True
            for times in range(1, self.patternlenth - 1):
                nextpattern = False
                nextelement = second - distance * times
                infochain.append(nextelement)
                if nextelement >= 0:
                    if self.inputchain[nextelement] == color:
                        nextpattern = True
                    else:
                        break
                else:
                    break

            if nextpattern:
                self.TextBrowser.append(color + "-Muster")
                textchain = self.inputchain[:]
                for element in infochain:
                    textchain[element] = "Muster"
                self.TextBrowser.append(str(textchain))
                self.pattern = color
                break

        if not self.pattern:
            self.Types[color].append(self.LastElement)
            self.pattern = False
            self.TextBrowser.append("Kein Muster!")
            self.TextBrowser.append(str(self.inputchain))

    ########################################################################################################################
    # Ketten-Generierungsalgorithmus
    ########################################################################################################################

    def Algorithm(self, mode, goal):
        self.alive = True
        while self.alive:

            # Zufälliges Element an Kette anhängen
            self.inputchain.append(self.colors[randint(0, len(self.colors) - 1)])

            # Untervariablen definieren
            self.LastElement = len(self.inputchain) - 1
            wrongstreak = 0
            self.pattern = True

            # Wiederhole, solange ein Muster in der Kette existiert
            while self.pattern:
                self.pattern = False

                # Muster-Erkennungsalgorithmus laufen lassen
                self.FindPattern()

                # Wenn keine möglichkeiten mehr, abbrechen
                wrongstreak += 1
                if wrongstreak > len(self.colors):
                    self.pattern = False
                    self.alive = False

                # Wenn Muster gefunden, letztes Element austauschen
                if self.pattern:
                    nextcolor = self.colors.index(self.pattern) + 1
                    if nextcolor < len(self.colors):
                        self.inputchain[self.LastElement] = self.colors[nextcolor]
                    else:
                        self.inputchain[self.LastElement] = self.colors[0]

        # Schluss-Nachricht und endgültige Länge anzeigen
        self.TextBrowser.append("Versuch Vorbei!")
        self.TextBrowser.append("Die endgültige Länge ist: " + str(len(self.inputchain)))

        # Ergebnisse anzeigen, Speichern und GUI Elemente zurücksetzen
        finallen = len(self.inputchain)
        if self.infomode == "Liste":
            if finallen == self.nextgoal:
                self.DisplayButton.setEnabled(True)
                self.DiagramButton.setEnabled(True)
                self.SortButton.setEnabled(True)
                self.SortoutButton.setEnabled(True)
                self.info.append(str(self.inputchain))
                self.chainlist.append(self.inputchain)
        else:
            if finallen > self.record:
                self.record = finallen
                self.info.clear()
                self.info.append("Bisheriger Längenrekord: " + str(finallen))
                self.info.append("Mit der Kette: " + str(self.inputchain))
                self.DisplayButton.setEnabled(True)
                self.DiagramButton.setEnabled(True)
                self.SortButton.setEnabled(True)
                self.SortoutButton.setEnabled(True)
                self.chainlist = [self.inputchain]

        if mode == "SoOftBis":
            if finallen >= goal:
                self.done = True
                self.TextBrowser.append("die gewünschte Länge: " + str(goal) + " wurde erreicht!")
                self.TextBrowser.append("Es hat " + str(self.attempts) + " Versuche gebraucht")
        elif mode == "EinDurchlauf":
            self.done = True
            self.TextBrowser.append("Durchlauf vorbei!")
        if self.done:
            self.status = False
            self.Stop.setEnabled(False)
            self.Pause.setEnabled(False)
            self.Start.setEnabled(True)

        if self.cleartimer > 1000:
            self.TextBrowser.clear()
            self.cleartimer = 0

########################################################################################################################
# Hauptfenster öffnen
########################################################################################################################

if __name__ == "__main__":
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
        window = Main()  # Create an instance of our class
        app.exec_()  # Start the application
