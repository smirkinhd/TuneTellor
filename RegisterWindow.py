import webbrowser
import sys
import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SpotReq import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Authorization is succeed! You can close this window.')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing authorization code.')

def get_auth_code():
    auth_url = (
        'https://accounts.spotify.com/authorize?'
        'response_type=code&'
        f'client_id={SPOTIFY_CLIENT_ID}&'
        f'redirect_uri={SPOTIFY_REDIRECT_URI}&'
        'scope=user-read-private user-read-email'
    )
    webbrowser.open(auth_url)

    httpd = HTTPServer(('localhost', 8888), SpotifyAuthHandler)
    httpd.handle_request()
    return httpd.auth_code

# Функция для получения токена доступа
def get_spotify_token(auth_code):
    auth_str = f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': SPOTIFY_REDIRECT_URI
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.json().get('access_token')


class CustomButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("АВТОРИЗИРОВАТЬСЯ")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                width: 180px;
                height: 60px;
                font-size: 18px;
                font-weight: 100;
                color: white;
                border: 1px solid #91C9FF;
                background: transparent;
                transition: background 1s ease-in-out;
                border-radius: 20px;
            }
            QPushButton:hover {
                background: #4F95DA;
            }
        """)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(0, 0, 180, 60))
        self.animation.setEndValue(QRect(0, 0, 180, 60))


class RegisterPage(QWidget):
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

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(270, 200, 500, 400))
        self.frame.setStyleSheet("background-color: transparent;\n"
                                 "border-radius: 20px;"
                                 "border: 3px solid white;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame1")

        self.auth_text = QLabel(
            'Чтобы продолжить, необходимо \nпройти авторизацию\nУбедитесь, что Вы предварительно\nвключили VPN-сервис',
            self)
        self.auth_text.setGeometry(120, 220, 800, 160)
        self.auth_text.setStyleSheet("color: white;\n"
                                     "font: 10 16pt \"Unbounded Light\";")
        self.auth_text.setAlignment(Qt.AlignCenter)

        self.button_auth = CustomButton(self)
        self.button_auth.setGeometry(380, 400, 271, 71)
        self.button_auth.clicked.connect(self.on_button_auth_click)

    def on_button_auth_click(self):
        print("Кнопка АВТОРИЗИРОВАТЬСЯ нажата")
        self.authenticate_spotify()

    def authenticate_spotify(self):
        auth_url = (
            'https://accounts.spotify.com/authorize?'
            'response_type=code&'
            f'client_id={SPOTIFY_CLIENT_ID}&'
            f'redirect_uri={SPOTIFY_REDIRECT_URI}&'
            'scope=user-read-private user-read-email'
        )
        webbrowser.open(auth_url)

        httpd = HTTPServer(('localhost', 8888), SpotifyAuthHandler)
        httpd.handle_request()

        auth_code = httpd.auth_code
        token = self.get_spotify_token(auth_code)
        if token:
            # Check if it's the first time the app is launched
            parent_widget = self.parentWidget()
            if os.path.exists('first_launch.flag'):
                if parent_widget:
                    parent_widget.setCurrentIndex(parent_widget.currentIndex() + 1)


    def get_spotify_token(self, auth_code):
        auth_str = f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            'Authorization': f'Basic {b64_auth_str}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': SPOTIFY_REDIRECT_URI
        }

        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        return response.json().get('access_token')


