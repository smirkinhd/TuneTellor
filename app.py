import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from CheckInternetPage import LoadingPage
from StartScreen import StartPage
from RegisterWindow import RegisterPage
from WorkFields import WorkPlace

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=3000)
        print("Подключение к интернету есть")
        return True
    except requests.ConnectionError:
        print("Нет подключения к интернету")
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        height = 768
        self.setFixedHeight(height)
        width = 1024
        self.setFixedWidth(width)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.setWindowTitle('TuneTellor - Практическая часть ВКР 2024')
        self.setWindowIcon(QIcon('src/iconka.png'))

        # Создаем экземпляры страниц
        self.page1 = LoadingPage(self.stacked_widget)
        self.page2 = StartPage(self.stacked_widget)
        self.page3 = RegisterPage(self.stacked_widget)
        self.page4 = WorkPlace(self.stacked_widget)

        # Добавляем страницы в QStackedWidget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.addWidget(self.page4)

        # Проверка соединения с интернетом
        if check_internet_connection():
            # Устанавливаем таймер на 3 секунды (3000 миллисекунд)
            self.timer = QTimer(self)
            self.timer.setInterval(3000)  # 3000 миллисекунд = 3 секунды
            self.timer.timeout.connect(self.switch_page)
            self.timer.start()
        else:
            self.show_no_internet_message()

    def switch_page(self):
        # Переключаемся на следующую страницу
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)

        # Останавливаем таймер после первого переключения
        self.timer.stop()

    def show_no_internet_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Нет подключения к интернету")
        msg.setText("Пожалуйста, проверьте ваше интернет-соединение и попробуйте снова.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.close_app)
        msg.exec_()

    def close_app(self):
        sys.exit(404)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
