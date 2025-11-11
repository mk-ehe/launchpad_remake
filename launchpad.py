from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QApplication, QWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl, Qt, QLoggingCategory
import sys, os

from random import choice

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 80, 750, 790)
        self.setFixedSize(750, 790)
        self.setWindowTitle("Launchpad")
        self.setWindowIcon(QIcon("daszi_icon.png"))
        
        self.buttons = {}
        self.sounds = {}
        
        self.key_map = {
            Qt.Key.Key_0: '0',
            Qt.Key.Key_1: '1',
            Qt.Key.Key_2: '2',
            Qt.Key.Key_3: '3',
            Qt.Key.Key_4: '4',
            Qt.Key.Key_5: '5',
            Qt.Key.Key_6: '6',
            Qt.Key.Key_7: '7',
            Qt.Key.Key_8: '8',
            Qt.Key.Key_9: '9',
        }

        self.button_colors = [
            "RoyalBlue",
            "CornflowerBlue",
            "SkyBlue",
            "Teal",
            "MediumSeaGreen",
            "LimeGreen",
            "Gold",
            "Orange",
            "Coral",
            "Crimson",
            "MediumOrchid",
            "BlueViolet",
            "Plum",
            "SlateBlue",
            "DodgerBlue"
            ]

        self.setStyleSheet("""QPushButton{
                    font-size: 25px;
                    font-family: Arial;
                    font-weight: bold;
                    border: 3px solid;
                    border-radius: 14px
                    }""")
                        
        self.gridInit()
        self.soundInit()
        
        bg = QLabel(self)
        bg.setGeometry(0, 0, 750, 790)
        pixmap = QPixmap("daszi.png")
        bg.setPixmap(pixmap)
        bg.setScaledContents(True)
        bg.lower()

    def gridInit(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid = QGridLayout(central_widget)
        grid.setSpacing(10)

        for i in range(10):
            btn = QPushButton(str(i))
            btn.setFixedSize(180, 180)
            self.buttons[str(i)] = btn

            if i != 0:
                self.buttons[str(i)].setStyleSheet(f"""background: qlineargradient(
                                                x1:0, y1:0, x2:0, y2:1,
                                                stop:0 {choice(self.button_colors)},
                                                stop:1 {choice(self.button_colors)});
                                                """)
            else:
                self.buttons[str(i)].setStyleSheet(f"""background-color: white""")
                    
        self.buttons['0'].setFixedSize(180, 60)

        positions = [
            (0, 0, "7"), (0, 1, "8"), (0, 2, "9"),
            (1, 0, "4"), (1, 1, "5"), (1, 2, "6"),
            (2, 0, "1"), (2, 1, "2"), (2, 2, "3"),
            (3, 1, "0")
        ]

        for row, col, btn in positions:
            grid.addWidget(self.buttons[btn], row, col)


    def soundInit(self):
        for i in range(10):
            wav_path = f"sounds\\{i}.wav"
            if not os.path.exists(wav_path):
                print(f"File not found: {wav_path}")
                continue

            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(wav_path))
            sound.setVolume(0.5)

            if i == 0:
                sound.setVolume(0.3)

            self.sounds[str(i)] = sound
            self.buttons[str(i)].clicked.connect(lambda _, key=str(i): self.playSound(key))


    def keyPressEvent(self, event):
        if event.isAutoRepeat():        # nie ma spamu przy podczas przytrzymania przycisku
            return
            
        key = event.key()
        if key in self.key_map:
            btn_key = self.key_map[key]
            
            if btn_key in self.buttons:
                self.buttons[btn_key].setDown(True)
                if self.buttons[btn_key].text() != '0':
                    if event.isAutoRepeat():
                        return
                    self.buttons[btn_key].setStyleSheet(f"""background: qlineargradient(
                                                        x1:0, y1:0, x2:0, y2:1,
                                                        stop:0 {choice(self.button_colors)},
                                                        stop:1 {choice(self.button_colors)});
                                                        """)     
            self.playSound(btn_key)
        
        super().keyPressEvent(event)    # tutaj nic nie robi, ale normalnie obsługuje skróty klawiszowe itd. ogólnie logika Qt


    def keyReleaseEvent(self, event):
        key = event.key()
        if key in self.key_map:
            btn_key = self.key_map[key]
            if btn_key in self.buttons:
                self.buttons[btn_key].setDown(False)


    def playSound(self, key):
        sound = self.sounds.get(key)
        if sound:
            if key == '0':
                if sound.isPlaying():
                    sound.stop()
            sound.play()


if __name__ == "__main__":
    QLoggingCategory.setFilterRules("qt.multimedia.*=false")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()