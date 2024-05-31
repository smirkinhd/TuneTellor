import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping
from keras.regularizers import l2
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from annoy import AnnoyIndex

# Загрузка данных из большого датасета
dataset_path = '/content/dataset.csv'  # Укажите путь к вашему датасету
df = pd.read_csv(dataset_path)

# Предполагаем, что датасет имеет столбцы: 'track_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
track_features_dataset = df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']].values

# Разделение данных на тренировочный и валидационный наборы
train_features, val_features = train_test_split(track_features_dataset, test_size=0.2, random_state=42)
scaler = StandardScaler()
train_features = scaler.fit_transform(train_features)
val_features = scaler.transform(val_features)
track_features_dataset = scaler.transform(track_features_dataset)

# Определение и обучение модели автоэнкодера
model = Sequential([
    Dense(128, activation='relu', input_shape=(train_features.shape[1],), kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(64, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(32, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dense(train_features.shape[1], activation='linear')
])

model.compile(optimizer='adam', loss='mse')

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

history = model.fit(train_features, train_features, epochs=200, batch_size=64, validation_data=(val_features, val_features), callbacks=[early_stopping])

# Преобразование фич с помощью обученной нейросети
transformed_features = model.predict(track_features_dataset)

um_features = transformed_features.shape[1]
annoy_index = AnnoyIndex(num_features, 'angular')

# Добавление фич в AnnoyIndex
for i in range(len(transformed_features)):
    annoy_index.add_item(i, transformed_features[i])

# Построение дерева
annoy_index.build(10)