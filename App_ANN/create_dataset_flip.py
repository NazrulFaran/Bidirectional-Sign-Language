import os
import pickle
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    min_detection_confidence=0.3
)

DATA_DIR = './data'

data = []
labels = []

def process_image(img_rgb, label):
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []
            x_ = []
            y_ = []

            for lm in hand_landmarks.landmark:
                x_.append(lm.x)
                y_.append(lm.y)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

            data.append(data_aux)
            labels.append(label)

for dir_ in os.listdir(DATA_DIR):
    class_dir = os.path.join(DATA_DIR, dir_)
    for img_path in os.listdir(class_dir):
        img = cv2.imread(os.path.join(class_dir, img_path))
        if img is None:
            continue

        # ---------- Original image ----------
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        process_image(img_rgb, dir_)

        # ---------- Horizontally flipped image ----------
        img_flipped = cv2.flip(img, 1)  # 1 = horizontal flip
        img_flipped_rgb = cv2.cvtColor(img_flipped, cv2.COLOR_BGR2RGB)
        process_image(img_flipped_rgb, dir_)

# Save dataset
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Dataset created with flipped images included!")
