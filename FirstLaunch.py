import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ToggleSwitch(QCheckBox):
    def __init__(self, text, parent=None):
        super(ToggleSwitch, self).__init__(text, parent)
        self.setChecked(False)
        self.setFont(QFont('Unbounded Light', 10, QFont.Bold))
        self.setStyleSheet(self.styleSheetTemplate())


    def styleSheetTemplate(self):
        return """
        QCheckBox {
            outline: 0;
            width: 4em;
            height: 2em;
            position: relative;
            cursor: pointer;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            color: white;
        }
        QCheckBox::indicator {
            width: 3em;
            height: 2em;
        }
        QCheckBox::indicator:unchecked {
            background-color: transparent;
            color: #fff;
            border: 3px solid white;
            border-radius: 4px;
            line-height: 2em;
            text-align: center;
            font-family: sans-serif;
            font-weight: bold;
            transition: all 0.4s ease;
        }
        QCheckBox::indicator:checked {
            background-color: white;
            color: black;
            border: 3px solid white;
            border-radius: 4px;
            line-height: 2em;
            text-align: center;
            font-family: sans-serif;
            font-weight: bold;
            transition: all 0.4s ease;
        }
        """

class CustomButton(QPushButton):
    def __init__(self, parent=None):
        super(CustomButton, self).__init__(parent)
        self.setObjectName("CustomButton")
        self.setText("Продолжить!")
        self.setCursor(QCursor(Qt.PointingHandCursor))
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

class FirstLaunch(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.setupUi()

    def setupUi(self):
        height = 768
        self.setFixedHeight(height)
        width = 1024
        self.setFixedWidth(width)
        label = QLabel(self)
        label.setGeometry(0, 0, 1024, 768)
        self.centralwidget = QWidget(self)
        movie = QMovie('src/background.gif')
        label.setMovie(movie)
        movie.start()

        label.setScaledContents(True)

        dark_overlay = QLabel(self)
        dark_overlay.setGeometry(0, 0, 1024, 768)
        dark_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.65);")

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        label.setGraphicsEffect(blur_effect)

        self.Oglavlenie = QLabel("Выберите жанры, которые вам подходят больше", self)
        self.Oglavlenie.setGeometry(130, 10, 800, 160)
        self.Oglavlenie.setStyleSheet("color: white;\n"
                                      "font: 10 18pt \"Unbounded Medium\";")
        self.Oglavlenie.setAlignment(Qt.AlignCenter)

        self.Opisanie = QLabel("Исходя из вашего выбора, мы сможем проанализировать ваши композиции и подобрать то, \nчто вы ищите - хорошую музыку, которая будет радовать ваши уши", self)
        self.Opisanie.setGeometry(85, 70, 900, 160)
        self.Opisanie.setStyleSheet("color: white;\n"
                                      "font: 12 12pt \"Unbounded ExtraLight\";")
        self.Opisanie.setAlignment(Qt.AlignCenter)

        self.line = QFrame(self)
        self.line.setGeometry(QRect(130, 200, 800, 3))
        self.line.setStyleSheet("background-color: white;")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)


        self.toggle1 = ToggleSwitch("Рок-музыка", self)
        self.toggle1.setGeometry(130, 200, 271, 71)

        self.toggle2 = ToggleSwitch("Поп-музыка", self)
        self.toggle2.setGeometry(320, 200, 271, 71)

        self.toggle3 = ToggleSwitch("Класическая \nмузыка", self)
        self.toggle3.setGeometry(510, 200, 271, 71)

        self.toggle4 = ToggleSwitch("Электронная \nмузыка", self)
        self.toggle4.setGeometry(700, 200, 271, 71)

        #нижний ряд
        self.toggle5 = ToggleSwitch("Латинская \nмузыка", self)
        self.toggle5.setGeometry(235, 275, 271, 71)

        self.toggle6 = ToggleSwitch("Хип-хоп \nмузыка", self)
        self.toggle6.setGeometry(445, 275, 271, 71)
        #
        self.toggle7 = ToggleSwitch("Разное", self)
        self.toggle7.setGeometry(615, 275, 271, 71)

        self.button_continue = CustomButton(self)
        self.button_continue.setGeometry(325, 500, 400, 50)
        self.button_continue.clicked.connect(self.on_button_click)

    def on_button_click(self):
        parent_widget = self.parentWidget()
        if parent_widget:
            parent_widget.setCurrentIndex(parent_widget.currentIndex() + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    window = FirstLaunch(stacked_widget)
    window.show()
    sys.exit(app.exec_())





