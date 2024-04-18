import json
import ast
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

# Load and process the data
with open('./Data_Processing/frames.json', "r") as f:
    json_data = json.load(f)

df = pd.DataFrame(json_data)
X = np.array(df['frame'])
X_processed = []
for i, frame in enumerate(X):
    print(i)
    frame_temp = [ast.literal_eval(list) for list in frame]
    X_processed.append(frame_temp)
X = np.array(X_processed)
y = np.array(df['label'])
print(f"Y with len of {y.shape} and X with len of {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=False, random_state=42)

# Define the model
def create_model(filters=(16, 32), kernel_size=(3, 5), learning_rate=0.001):
    model = Sequential([
        Conv1D(filters=filters[0], kernel_size=kernel_size[0], activation='relu', input_shape=(X_train[1].shape[0],7), name="input"),
        MaxPooling1D(2),
        Flatten(),
        Dense(10, activation='relu'),
        Dense(5, activation="softmax", name="output")
    ])

    # Compile the model with the provided learning rate
    model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), metrics=['accuracy'])
    return model

# Define the hyperparameter grid for GridSearchCV
param_grid = {
  'filters': [(16, 32), (32, 64)],  # Try different filter configurations
  'kernel_size': [(3, 5), (5, 7)],  # Experiment with kernel sizes
  'learning_rate': [0.001, 0.01]  # Explore different learning rates
}

# Wrap the create_model function for scikit-learn compatibility
wrapped_model = KerasClassifier(build_fn=create_model, verbose=1)

# Create the GridSearchCV object
grid_search = GridSearchCV(estimator=wrapped_model, param_grid=param_grid, cv=5)

# Train the model with GridSearch
grid_search.fit(X_train, y_train)

# Access the best model and its parameters
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

# Evaluate the best model on the test set
test_loss, test_acc = best_model.evaluate(X_test, y_test)

print("Best Hyperparameters:", best_params)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_acc)
