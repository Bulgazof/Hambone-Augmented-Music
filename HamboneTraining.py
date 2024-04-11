from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Define model parameters
num_frames = 50
frame_dim = 4  # Assuming each frame has 4 integer values
num_classes = 5  # Prediction between 1 and 5

# Create the model
model = Sequential()
model.add(LSTM(units=16, return_sequences=False, input_shape=(num_frames, frame_dim)))
model.add(Dense(units=num_classes, activation="softmax"))

# Compile the model (adjust optimizer considering ESP32 limitations)
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Prepare your training data
# This part assumes you have your data preprocessed with 50 frames of 4 integers each
# and corresponding labels between 1 and 5.
# X_train: array of shape (num_samples, num_frames, frame_dim)
# y_train: array of shape (num_samples,) containing labels

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Use the model for prediction
# new_data: array of shape (1, num_frames, frame_dim) containing 50 frames of data
prediction = model.predict(new_data)

# prediction will be an array of probabilities for each class (1 to 5)
# You can choose the class with the highest probability

# Example: get the index of the class with highest probability
predicted_class = np.argmax(prediction[0]) + 1  # Add 1 to get class between 1 and 5
print("Predicted class:", predicted_class)
