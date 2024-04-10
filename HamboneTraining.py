from tensorflow.keras.models import Sequential
from tensorflow.keras import layers


# Number of frames per element
num_frames = 50
features_per_frame = 3

input_shape = (num_frames, features_per_frame)

model = Sequential()[
    layers.LSTM(units=5, return_sequences=True, input_shape=input_shape),
    layers.dense(4, activation='sigmoid')
]