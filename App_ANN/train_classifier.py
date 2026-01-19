import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras import layers, models

def create_improved_model(input_shape=(42,), num_classes=26):
    model = models.Sequential([
        layers.Dense(256, activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# Load your collected data
data_dict = pickle.load(open('./data.pickle', 'rb'))
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

print(f"Dataset shape: {data.shape}")
print(f"Labels: {np.unique(labels)}")
print(f"Samples per class: {np.unique(labels, return_counts=True)[1]}")

# Encode labels to integers
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Split data
x_train, x_test, y_train, y_test = train_test_split(
    data, labels_encoded, test_size=0.2, shuffle=True, stratify=labels_encoded, random_state=42
)

print(f"Training samples: {len(x_train)}")
print(f"Testing samples: {len(x_test)}")

# Create and train model
model = create_improved_model(input_shape=(data.shape[1],), 
                             num_classes=len(np.unique(labels_encoded)))

# Add callbacks for better training
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=15, restore_best_weights=True),
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=10)
]

# Train the model
history = model.fit(
    x_train, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(x_test, y_test),
    callbacks=callbacks,
    verbose=1
)

# Evaluate final model
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f'\nFinal Test Accuracy: {test_accuracy * 100:.2f}%')

# Save the improved model and label encoder
model.save('improved_hand_model.h5')
with open('label_encoder.pickle', 'wb') as f:
    pickle.dump({'label_encoder': label_encoder, 'classes': label_encoder.classes_}, f)

print("Model and label encoder saved successfully!")