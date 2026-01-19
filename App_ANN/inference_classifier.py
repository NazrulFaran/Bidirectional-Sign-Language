import pickle
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import winspeech
from collections import deque
import threading

class HandSignRecognizer:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.cap = None
        self.hands = None
        self.detected_words = []
        
        # Configurable variables
        self.required_continuous_frames = 20
        self.confidence_threshold = 0.7
        self.frame_history = deque(maxlen=self.required_continuous_frames)
        self.last_spoken_char = None
        self.cooldown_frames = 20
        self.cooldown_counter = 0
        
        # TTS control
        self.tts_lock = threading.Lock()
        self.is_speaking = False
        
        self.setup_tts()
        self.load_model()
        self.setup_camera()

    # ================= BACKSPACE =================
    def handle_backspace(self):
        """Delete last detected character"""
        if self.detected_words:
            removed = self.detected_words.pop()
            print(f"⌫ Backspace removed: '{removed}'")
        else:
            print("⌫ Backspace detected but nothing to delete")

    # ================= TTS =================
    def setup_tts(self):
        try:
            winspeech.say("Test")
        except:
            pass

    def speak_text(self, text):
        try:
            winspeech.say(text)
        except:
            pass

    # ================= MODEL =================
    def load_model(self):
        self.model = tf.keras.models.load_model('improved_hand_model.h5')
        label_dict = pickle.load(open('label_encoder.pickle', 'rb'))
        self.label_encoder = label_dict['label_encoder']

        print("✅ Model loaded")
        print("📊 Classes:", list(self.label_encoder.classes_))

    # ================= CAMERA =================
    def setup_camera(self):
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    # ================= CONTINUOUS CHECK =================
    def check_continuous_detection(self, char, confidence):
        if confidence >= self.confidence_threshold:
            self.frame_history.append(char)
        else:
            self.frame_history.append(None)

        if len(self.frame_history) < self.required_continuous_frames:
            return False

        return all(x == char and x is not None for x in self.frame_history)

    # ================= FRAME PROCESS =================
    def process_frame(self, frame):
        H, W = frame.shape[:2]

        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
            if self.cooldown_counter == 0:
                self.last_spoken_char = None

        side = max(H, W)
        frame_square = np.zeros((side, side, 3), dtype=np.uint8)
        frame_square[:H, :W] = frame
        frame_rgb = cv2.cvtColor(frame_square, cv2.COLOR_BGR2RGB)

        results = self.hands.process(frame_rgb)

        current_prediction = None
        current_confidence = 0
        detection_status = "Show Your Hand"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                self.mp_drawing.draw_landmarks(
                    frame_square,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

                x_ = [lm.x for lm in hand_landmarks.landmark]
                y_ = [lm.y for lm in hand_landmarks.landmark]

                data_aux = []
                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))

                if len(data_aux) == 42:
                    prediction = self.model.predict(np.array([data_aux]), verbose=0)
                    predicted_class = np.argmax(prediction)
                    confidence = np.max(prediction)

                    x1 = int(min(x_) * side) - 20
                    y1 = int(min(y_) * side) - 20
                    x2 = int(max(x_) * side) + 20
                    y2 = int(max(y_) * side) + 20

                    if confidence > 0.5:
                        predicted_label = self.label_encoder.inverse_transform([predicted_class])[0]
                        current_prediction = predicted_label
                        current_confidence = confidence

                        box_color = (0, 255, 0) if confidence > self.confidence_threshold else (0, 165, 255)
                        self.draw_rounded_rect(frame_square, (x1, y1), (x2, y2), box_color, 2, radius=15)

                        label_text = f'{predicted_label} ({confidence:.2f})'
                        self.draw_gradient_background(frame_square, label_text, (x1, y1),
                                                      bg_color=(0, 0, 0), text_color=box_color)

                        self.draw_confidence_bar(frame_square, confidence, (x1, y2 + 10))

                        if confidence >= self.confidence_threshold and self.cooldown_counter == 0:
                            is_continuous = self.check_continuous_detection(current_prediction, current_confidence)

                            if is_continuous:

                                # ===== BACKSPACE OR NORMAL CHARACTER =====
                                if current_prediction == '0':
                                    self.handle_backspace()
                                    detection_status = "Backspace"
                                else:
                                    self.speak_text(current_prediction)
                                    self.detected_words.append(current_prediction)
                                    detection_status = f"Detected: {current_prediction}!"

                                self.last_spoken_char = current_prediction
                                self.cooldown_counter = self.cooldown_frames
                                self.frame_history.clear()

                                print(f"📝 Current words: {''.join(self.detected_words)}")

                            else:
                                progress = len([x for x in self.frame_history if x == current_prediction and x is not None])
                                detection_status = f"Detecting: {current_prediction} ({progress}/{self.required_continuous_frames})"
                        elif self.cooldown_counter > 0:
                            detection_status = f"Cooldown: {self.cooldown_counter} frames"
                        else:
                            detection_status = f"Low Confidence: {current_prediction}"

        # ================= UI (UNCHANGED) =================
        cv2.putText(frame_square, f"Words: {''.join(self.detected_words)}",
                    (20, H - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        status_color = (0,255,0) if "Detected:" in detection_status else (255,255,255)
        cv2.putText(frame_square, detection_status,
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

        settings_text = f"Settings: {self.required_continuous_frames} frames, {self.confidence_threshold*100}% confidence"
        cv2.putText(frame_square, settings_text,
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)

        instructions = "Press 'Q': Quit | 'C': Clear | 'S': Speak Words | 'Enter': Add Space"
        cv2.putText(frame_square, instructions,
                    (20, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)

        return frame_square[:H, :W]

    # ================= DRAWING =================
    def draw_rounded_rect(self, img, pt1, pt2, color, thickness, radius=20):
        x1, y1 = pt1
        x2, y2 = pt2
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

    def draw_gradient_background(self, frame, text, position, bg_color, text_color):
        x, y = position
        cv2.putText(frame, text, (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

    def draw_confidence_bar(self, frame, confidence, position, width=200, height=20):
        x, y = position
        fill_width = int(width * confidence)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (50,50,50), -1)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), (0,255,0), -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255,255,255), 2)

    # ================= MAIN LOOP =================
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame)
            cv2.imshow("✨ AI Hand Sign Recognition with TTS", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.detected_words.clear()
            elif key == ord('s'):
                if self.detected_words:
                    self.speak_text(''.join(self.detected_words))
            elif key == 13:
                self.detected_words.append(' ')

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Final words:", ''.join(self.detected_words))


if __name__ == "__main__":
    HandSignRecognizer().run()
