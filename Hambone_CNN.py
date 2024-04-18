from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv1D
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import json
import os
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


with open('./Data_Processing/frames.json', "r") as f:
    json_data = json.load(f)

df = pd.DataFrame(json_data)
X = np.array(df['frame'])
X_processed = []
i = 0
for frame in X:
    print(i)
    i+=1
    frame_temp = []
    for list in frame:
        temp = ast.literal_eval(list)
        frame_temp.append(temp)
    X_processed.append(frame_temp)
X = np.array(X_processed)
y = np.array(df['label'])
print(f"Y with len of {y.shape} and X with len of {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=False, random_state=42)

model_CNN = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(20,3,activation='relu',input_shape=(X_train[1].shape[0],7),name="input"),
    tf.keras.layers.MaxPooling1D(2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(10,activation='relu'),
    tf.keras.layers.Dense(5, activation="softmax", name="output")
])

model_CNN.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

from matplotlib import pyplot as plt

history = model_CNN.fit(
    X_train,
    y_train,
    epochs=10,
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
y_pred = model_CNN.predict(X_test)
y_chosen = []
for pred in y_pred:
    y_chosen.append(np.argmax(pred))
print(y_chosen[:100])
cnf_matrix = confusion_matrix(y_test, y_chosen)

print(model_CNN.predict(X_test[:1]))

plt.title("CNN with 10 Epochs")
cm = confusion_matrix(y_test, y_chosen)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

model_CNN.save('cnn_model.keras')  # Save the model after training

