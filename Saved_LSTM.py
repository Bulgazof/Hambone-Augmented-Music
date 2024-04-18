import tensorflow as tf
import json
import pandas as pd
import ast
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


model = tf.keras.models.load_model("lstm_model.keras")
with open('./Data_Processing/frames.json', "r") as f:
    json_data = json.load(f)

df = pd.DataFrame(json_data)
X = np.array(df['frame'])
X_processed = []
for frame in X:
    frame_temp = []
    for list in frame:
        temp = ast.literal_eval(list)
        frame_temp.append(temp)
    X_processed.append(frame_temp)
X = np.array(X_processed)
y = np.array(df['label'])
print(f"Y with len of {y.shape} and X with len of {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=False)
y_chosen = []
y_pred = model.predict(X_test)
for pred in y_pred:
    y_chosen.append(np.argmax(pred))

cm = confusion_matrix(y_test, y_chosen)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
