# Check Python version
import sys
print(f"Python version (should be 3.10.x): {sys.version}")

# Import libraries
import tensorflow as tf
import numpy as np
import sklearn
print(f"TensorFlow version (should be 2.15.x): {tf.__version__}")
print(f"Numpy version: {np.__version__}")
print(f"Scikit-learn version: {sklearn.__version__}")

# Setup the dataset, using MNIST digit data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize pixel values to 0-1
x_train = x_train / 255.
x_test = x_test / 255.

# Set the data up as numpy floats
x_train = x_train.astype(np.float32)
x_test = x_test.astype(np.float32)

# Create the TensorFlow LSTM model
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=x_train[0].shape, name="input"),
    tf.keras.layers.LSTM(20, return_sequences=True),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(10, activation="softmax", name="output")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
    )

model.summary()


# Train the model using the data
model.fit(
    x_train,
    y_train,
    epochs=5,
    validation_data=(x_test, y_test),
    batch_size=32
)

# Convert the model to have fixed input and output shapes
fixed_input = tf.keras.layers.Input(
    shape=x_train[0].shape,
    batch_size=1,
    dtype=model.inputs[0].dtype,
    name="fixed_input"
    )
fixed_output = model(fixed_input)

static_model = tf.keras.models.Model(fixed_input, fixed_output)
static_model.compile(optimizer='adam')

# Save the model as TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(static_model)
tflite_model = converter.convert()

# open("model.tflite", "wb").write(tflite_model)
