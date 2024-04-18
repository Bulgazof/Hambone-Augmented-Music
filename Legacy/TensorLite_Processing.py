import tensorflow as tf
import keras

model = tf.keras.models.load_model("cnn_model.keras")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.allow_custom_ops=True
converter.target_spec.supported_ops = [
tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)