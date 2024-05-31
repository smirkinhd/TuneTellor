from PyQt5.QtWidgets import QWidget, QLabel, QFrame
from PyQt5.QtCore import QTimer, Qt, QCoreApplication, QRect
from PyQt5.QtGui import QFont
import requests



class LoadingPage(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = None
        self.setupUi()

        def set_stacked_widget(self, stacked_widget):
            self.stacked_widget = stacked_widget

    def setupUi(self):
        self.setObjectName("TuneTellor")
        self.resize(1024, 768)
        self.setStyleSheet("background-color: black;")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(270, 200, 500, 400))
        self.frame.setStyleSheet("background-color: #D9D9D9;\n"
                                 "border-radius: 20px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        self.label = QLabel(self.frame)
        self.label.setGeometry(QRect(-60, 120, 611, 161))
        font = QFont()
        font.setFamily("Inter Thin")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi()


    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("TuneTellor", "TuneTellor"))
        self.label.setText(_translate("TuneTellor", "Подождите, \n"
                                                    "идёт проверка соединения"))
