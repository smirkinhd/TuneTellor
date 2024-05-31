from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os


class CustomButton(QPushButton):
    def __init__(self, parent=None):
        super(CustomButton, self).__init__(parent)
        self.setObjectName("CustomButton")
        self.setText("Приступить!")
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.setStyleSheet("""
            #CustomButton {
                width: 250px;
                height: 50px;
                line-height: 50px;
                font-weight: bold;
                text-decoration: none;
                background: #333;
                text-align: center;
                font-family: Unbounded;
                color: #fff;
                text-transform: uppercase;
                letter-spacing: 1px;
                border: 3px solid #333;
                border-radius: 20px;
            }
            #CustomButton:hover {
                width: 200px;
                border: 3px solid #2ecc71;
                background: transparent;
                color: #2ecc71;
            }
            #CustomButton .icon {
                width: 50px;
                height: 50px;
                border: 3px solid transparent;
                position: absolute;
                transform: rotate(45deg);
                right: 0;
                top: 0;
                z-index: -1;
            }
            #CustomButton .icon svg {
                width: 30px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: rotate(-45deg);
                fill: #2ecc71;
            }
            #CustomButton:hover .icon {
                border: 3px solid #2ecc71;
                right: -25%;
            }
        """)

class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        label = QLabel(self)
        label.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle("TuneTellor")
        movie = QMovie('src/background.gif')
        label.setMovie(movie)
        movie.start()

        label.setScaledContents(True)

        dark_overlay = QLabel(self)
        dark_overlay.setGeometry(0, 0, 1024, 768)
        dark_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.65);")  # Прозрачный черный цвет для затемнения

        font = QFont()
        font.setFamily("Krona One")
        font.setPointSize(64)

        self.oglavlenie = QLabel('TUNETELLOR', self)
        self.oglavlenie.setGeometry(130, 40, 800, 160)
        self.oglavlenie.setStyleSheet("color: white;\n"
                                      "font: 10 64pt \"Krona One\";")
        self.oglavlenie.setAlignment(Qt.AlignCenter)

        self.Opisanie = QLabel(
            'Программа реализует в себе нейронную сеть для анализа музыкальных предпочтений \nна основе аудиоаналитики с помощью языка Python\n\nДанная программа разработана в качестве выпускной квалификационной работы по теме \n“Применение нейронных сетей для определения музыкальных предпочтений”',
            self)
        self.Opisanie.setGeometry(10, 10, 1024, 550)
        self.Opisanie.setStyleSheet("color: white;\n"
                                    "font: 12pt \"Unbounded\";")
        self.Opisanie.setAlignment(Qt.AlignCenter)

        self.button_go = CustomButton(self)
        self.button_go.setGeometry(325, 500, 400, 50)
        self.button_go.clicked.connect(self.on_button_click)

    def on_button_click(self):
        print("Кнопка ПРИСТУПИТЬ нажата")
        parent_widget = self.parentWidget()
        if parent_widget:
            file_path = 'D:/TuneTellor/first_launch.flag'
            if os.path.isfile(file_path):
                parent_widget.setCurrentIndex(parent_widget.currentIndex() + 2)
                print("Проверка на flag. flag существует")
            else:
                parent_widget.setCurrentIndex(parent_widget.currentIndex() + 1)
                print("Проверка на flag. flag не существует")

