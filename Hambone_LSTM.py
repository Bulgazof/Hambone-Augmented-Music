# What exa
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv1D
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

data = pd.read_csv('./Data_Processing/frames.csv',index_col=0)

# Drop 'label' and 'thresh' columns (assuming they exist)
X_raw = np.array(data['coordinates'])
X_processed = []
for row in X_raw:
    temp = ast.literal_eval(row)
    X_processed.append(temp)

X_processed = np.array(X_processed)
y = np.array(data['label'])

def create_frames(data, frame_size=50):
    frames = []
    for i in range(len(data) - frame_size + 1):
        frame = data[i:i+frame_size]
        frames.append(frame)
    return frames

X = np.array(create_frames(X_processed))
y = np.array(y[49:])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=False)

# Define model parameters
num_frames = 1
frame_dim = 7  # Assuming each frame has 7 integer values
num_classes = 5  # Prediction between 1 and 5

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(50, frame_dim), name="input"),
    tf.keras.layers.LSTM(20, return_sequences=True),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(5, activation="softmax", name="output")
])

# Compile the model (adjust optimizer considering ESP32 limitations)
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

history = model.fit(
    X_train,
    y_train,
    epochs=3,
    validation_data=(X_test, y_test),
    batch_size=50
)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

y_pred = model.predict(X_test)
y_chosen = []
for pred in y_pred:
    y_chosen.append(np.argmax(pred))
print(y_chosen[:100])
cnf_matrix = confusion_matrix(y_test, y_chosen)

model.save('lstm_model.keras')  # Save the model after training

# print("Confusion Matrix:")
# print(cnf_matrix)
#
plt.title("LSTM with 10 Epochs")
cm = confusion_matrix(y_test, y_chosen)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

