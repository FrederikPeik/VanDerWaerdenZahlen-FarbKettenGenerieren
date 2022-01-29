# Van der Wearden Zahlen - Ketten generator
Ein simples User Interface zum generieren und bearbeiten, von Van Der Waerden Farbketten

## Inhalt
- Einleitung
- Technologies
- Setup
- Bedienelemente
- Status

## Einleitung
Dieses Programm ist im Rahmen eines Jugendforscht Projekts entwickelt worden. Es enthält einen Algorithmus zur Generierung kürzerer Van Der Waerden Zahlen. Der Satzt von van der Waerden ist ein Mathematische Problem, bei dem es darum geht aus einer bestimmten Anzahl (𝑟) verschiedener Elemente, die meist als Farben dargestellt werden, eine Möglichst lange Kette zu erzeugen. Dabei dürfen eine bestimmte Anzahl (𝑙) an Elementen der selben Farbe nicht in regelmäßigen Abständen zueinander stehen. Dieser Fall wird als Muster bezeichnet. Was für die unterschiedlichen Parameter (𝑟 und 𝑙) die Maximal länge einer Kette ohne Muster ist, ist nicht bekannt. Mit diesem Programm soll es möglich gemacht werden, mit unterschiedlichen Werten zu experimentieren und eigene Überlegungen anzustellen. 

## Technologies
##### Programmiersprache:
- Python 3.6
##### Bibleotheken
- PyQt5 5.15.6
- QDarkStyle 2.8.1
- pygame 2.1.2

## Setup
### Linux (Ubuntu)
- ##### Wenn Python noch nicht installiert: 
  ```sh
  sudo apt install python
- ##### Wenn Pip noch nicht installiert:
  ```sh
  sudo apt install pip
- ##### Benötigte Bibleotheken installieren: 
  ```sh
  pip install -r requirements.
- ##### Programm starten:
  ```sh
  python3 Main.py
### Windows
- ##### Wenn Python3 noch nicht installiert:
    1.Windows installer von der [Python download](https://www.python.org/downloads/release/python-3102/) seite herunterladen
    2.Installer öffnen und Python installieren
- ##### Wenn Pip noch nicht installiert:
    1.[get-pip.py](https://bootstrap.pypa.io/get-pip.py) herunterladen.
    2.Command line öffnen und ins Download Verzeichnis navigieren
        ```sh
        cd <Download Verzeichnis>
    3.Pip installieren
        ```sh
        python get-pip.py
- ##### Benötigte Bibleotheken installieren
    1.ins Projekt Verzeichnis navigieren
        ```sh
        cd <Projekt Verzeichnis>
    2.Bibleotheken installieren
        ```sh
        pip install -r requirements.txt
- ##### Programm starten
    ```sh
    python Main.py
