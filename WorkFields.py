import sys
import spotipy
import pandas as pd
import numpy as np
from keras.models import load_model
from keras.losses import mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
from spotipy import SpotifyOAuth
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from annoy import AnnoyIndex
from SpotReq import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

# Инициализация Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope='playlist-modify-public playlist-modify-private'))

# Загрузка данных и модели
data = pd.read_csv('dataset.csv')

label_encoders = {}
for column in ['artists', 'album_name', 'track_name', 'explicit', 'track_genre']:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

data = data.dropna()

# Предполагается, что ваш датасет содержит следующие колонки: 'danceability', 'energy', 'key', 'loudness', 'mode',
# 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
X = data[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
          'instrumentalness', 'liveness', 'valence', 'tempo']].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Загрузка модели с указанием пользовательской функции mean_squared_error
model = load_model("D:/TuneTellor/recomendation_model.h5", custom_objects={'mse': mean_squared_error})

# Использование автоэнкодера для преобразования фич
transformed_features = model.predict(X_scaled)

# Создание AnnoyIndex
num_features = transformed_features.shape[1]
annoy_index = AnnoyIndex(num_features, 'angular')

for i in range(len(transformed_features)):
    annoy_index.add_item(i, transformed_features[i])

annoy_index.build(10)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_audio_features(track_ids):
    features = sp.audio_features(track_ids)
    return pd.DataFrame(features)


def recommend_songs(input_song_features, annoy_index, scaler, top_n=100, noise_level=0.01):
    # Добавление случайного шума к входным признакам
    noise = np.random.normal(0, noise_level, input_song_features.shape)
    input_song_features_noisy = input_song_features + noise

    input_scaled = scaler.transform([input_song_features_noisy])
    input_transformed = model.predict(input_scaled)
    nearest_neighbors = annoy_index.get_nns_by_vector(input_transformed[0], top_n)

    # Уникальные индексы
    unique_neighbors = list(set(nearest_neighbors))
    return unique_neighbors[:top_n]



def recommend_from_playlist(playlist_id, annoy_index, scaler, top_n=100):
    tracks = get_playlist_tracks(playlist_id)
    track_ids = [track['track']['id'] for track in tracks]
    features_df = get_audio_features(track_ids)

    if features_df.empty:
        print("Не найдено аудио характеристик для треков в этом плейлисте.")
        return [], [], []

    required_columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    missing_columns = set(required_columns) - set(features_df.columns)

    for col in missing_columns:
        features_df[col] = 0

    input_features = features_df[required_columns].mean().values
    recommended_indices = recommend_songs(input_features, annoy_index, scaler, top_n)

    recommended_songs = data.iloc[recommended_indices]

    additional_info = []
    track_ids = []
    for idx in recommended_indices:
        track = data.iloc[idx]
        duration_ms = track['duration_ms']
        duration_min_sec = f"{int(duration_ms // 60000)}:{int((duration_ms % 60000) // 1000):02d}"
        track_ids.append(track['track_id'])
        additional_info.append({
            'artist': label_encoders['artists'].inverse_transform([track['artists']])[0],
            'track_name': label_encoders['track_name'].inverse_transform([track['track_name']])[0],
            'duration': duration_min_sec,
            'track_id': track['track_id']
        })

    unique_additional_info = []
    seen_tracks = set()
    count = 0
    for info in additional_info:
        if info['track_name'] not in seen_tracks and count < 10:
            unique_additional_info.append(info)
            seen_tracks.add(info['track_name'])
            count += 1

    return recommended_songs, unique_additional_info, track_ids[:10]  # Возвращаем только 10 track_ids



class CustomButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("СГЕНЕРИРОВАТЬ")
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

class WorkPlace(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.sp = sp  # Использование глобально инициализированного объекта Spotify
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
        dark_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.75);")

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        label.setGraphicsEffect(blur_effect)

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(20, 25, 982, 713)
        self.frame.setStyleSheet("background-color: transparent;\n"
                                 "border-radius: 20px;"
                                 "border: 3px solid white;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame1")

        self.titleName = QLabel("TUNE\nTELLOR", self)
        self.titleName.setGeometry(40, 40, 800, 160)
        self.titleName.setStyleSheet("color: white;\n"
                                     "font: 10 32pt \"Krona One\";")

        self.Opisanie = QLabel("Выберите свой плейлист", self)
        self.Opisanie.setGeometry(300, 35, 800, 50)
        self.Opisanie.setStyleSheet("color: white;\n"
                                    "font: 10 24pt \"Unbounded Light\";")

        self.playlist_combo = QComboBox(self)
        self.playlist_combo.move(300, 90)
        self.playlist_combo.resize(500, 50)
        self.playlist_combo.setStyleSheet("color: white;"
                                          "background-color: transparent;"
                                          "border-radius: 20px;"
                                          "border: 1px solid white;"
                                          "font: 10 12pt \"Unbounded ExtraLight\";")

        self.button_generate = CustomButton(self)
        self.button_generate.setGeometry(300, 160, 171, 45)
        self.button_generate.clicked.connect(self.button_generate_click)
        self.populate_playlists()

        self.line = QFrame(self)
        self.line.setGeometry(40, 220, 942, 3)
        self.line.setStyleSheet("background-color: white;")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.results_area = QScrollArea(self)
        self.results_area.setStyleSheet("background-color: transparent;"
                                        "font: 9 12pt \"Unbounded ExtraLight\";")
        self.results_area.setGeometry(40, 240, 942, 500)
        self.results_area.setWidgetResizable(True)
        self.results_content = QWidget()
        self.results_layout = QVBoxLayout(self.results_content)
        self.results_area.setWidget(self.results_content)

        self.button_save_all = CustomButton(self)
        self.button_save_all.setGeometry(550, 160, 171, 45)
        self.button_save_all.setText("Сохранить")
        self.button_save_all.clicked.connect(self.save_all_tracks)

    def populate_playlists(self):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            self.playlist_combo.addItem(playlist['name'], playlist['id'])

    def button_generate_click(self):
        playlist_id = self.playlist_combo.currentData()
        recommended_songs, additional_info, self.recommended_track_ids = recommend_from_playlist(playlist_id,
                                                                                                 annoy_index, scaler,
                                                                                                 top_n=100)

        # Очистка предыдущих результатов
        for i in reversed(range(self.results_layout.count())):
            widget_to_remove = self.results_layout.itemAt(i).widget()
            self.results_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Отображение новых рекомендаций (10 уникальных песен)
        for info in additional_info:
            song_label = QLabel(f"{info['artist']} - {info['track_name']} ({info['duration']})")
            song_label.setStyleSheet("color: white;")
            self.results_layout.addWidget(song_label)

        self.results_content.setLayout(self.results_layout)

    def save_all_tracks(self):
        user_id = self.sp.current_user()['id']
        playlist_name = "Сгенерировано TuneTellor"

        # Check if the playlist already exists
        playlists = self.sp.current_user_playlists()
        playlist_id = None
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break

        # If the playlist does not exist, create it
        if not playlist_id:
            new_playlist = self.sp.user_playlist_create(user_id, playlist_name, public=False)
            playlist_id = new_playlist['id']

        # Add the recommended tracks to the playlist, avoiding duplicates
        if hasattr(self, 'recommended_track_ids') and self.recommended_track_ids:
            # Get current track IDs in the playlist
            current_tracks = self.sp.playlist_tracks(playlist_id)
            current_track_ids = [track['track']['id'] for track in current_tracks['items']]

            # Filter out duplicates and save only the displayed tracks (10 unique tracks)
            unique_track_ids = list(set(self.recommended_track_ids) - set(current_track_ids))

            if unique_track_ids:
                self.sp.playlist_add_items(playlist_id, unique_track_ids)
                QMessageBox.information(self, "Success", "Tracks have been saved to your playlist.")
            else:
                QMessageBox.information(self, "No New Tracks", "No new tracks to add to the playlist.")
        else:
            QMessageBox.warning(self, "No Tracks", "No recommended tracks to save.")




