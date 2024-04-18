import tensorflow as tf
import json
import pandas as pd
import ast
import numpy as np
from sklearn.model_selection import train_test_split



with open('./Data_Processing/frames.json', "r") as f:
    json_data = json.load(f)

model = tf.keras.models.load_model("cnn_model.keras")

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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=False)

print(np.argmax(model.predict(X_train[:1])))

print(f"Shape {X_train[:1].shape}: Type {type(X_train[:1])}")

