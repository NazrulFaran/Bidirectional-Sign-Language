import pickle
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import winspeech
from collections import deque
import threading
import time
import serial
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys

# ================== GLOBAL CONFIG ==================

# Vosk model
VOSK_MODEL_PATH = r"E:\Gesture_ANN\vosk-model-small-en-us-0.15"

# Serial ESP32
SERIAL_PORT = "COM7"
BAUD_RATE = 115200

# Audio (Vosk)
SAMPLE_RATE = 16000
BLOCK_DURATION_MS = 30  # ms

# Delay between letters when running voice→servo sequence
LETTER_INTERVAL_SEC = 8.0  # <<< changed to 8 seconds

# Max letters allowed from voice
MAX_VOICE_LETTERS = 6

# ===================================================


class HandSignRecognizer:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.cap = None
        self.hands = None
        self.detected_words = []

        # Detection stability
        self.required_continuous_frames = 20
        self.confidence_threshold = 0.7
        self.frame_history = deque(maxlen=self.required_continuous_frames)
        self.last_spoken_char = None
        self.cooldown_frames = 20
        self.cooldown_counter = 0

        # TTS
        self.tts_lock = threading.Lock()
        self.is_speaking = False

        # Vosk / Serial
        self.vosk_model = None
        self.vosk_recognizer = None
        self.ser = None

        # Window name (for full screen)
        self.window_name = "✨ AI Hand Sign Recognition with TTS"

        # Main-loop running flag (for button1 = quit)
        self.running = True

        self.setup_tts()
        self.load_model()
        self.setup_camera()
        self.setup_vosk()
        self.setup_serial()

    # ============== TTS ==================
    def setup_tts(self):
        try:
            winspeech.say("Test")
        except Exception:
            pass

    def speak_text(self, text):
        try:
            winspeech.say(text)
        except Exception as e:
            print("TTS error:", e)

    # ============== Hand model ============
    def load_model(self):
        self.model = tf.keras.models.load_model('improved_hand_model.h5')
        label_dict = pickle.load(open('label_encoder.pickle', 'rb'))
        self.label_encoder = label_dict['label_encoder']
        print("✅ Hand model loaded")
        print("📊 Classes:", list(self.label_encoder.classes_))

    # ============== Camera / Mediapipe ============
    def setup_camera(self):
        # Try camera 0, then 1 if needed
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Camera 0 failed, trying camera 1...")
            self.cap = cv2.VideoCapture(1)

        if not self.cap.isOpened():
            print("❌ No camera available! Check connection.")
            self.cap = None
            return

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

    # ============== Vosk ==================
    def setup_vosk(self):
        print("Loading Vosk model... (this may take a few seconds)")
        try:
            self.vosk_model = Model(VOSK_MODEL_PATH)
            self.vosk_recognizer = KaldiRecognizer(self.vosk_model, SAMPLE_RATE)
            print("✅ Vosk model loaded")
        except Exception as e:
            print("⚠️ Failed to load Vosk model:", e)
            self.vosk_model = None
            self.vosk_recognizer = None

    # ============== Serial ==================
    def setup_serial(self):
        print(f"Opening serial port {SERIAL_PORT} at {BAUD_RATE} baud...")
        try:
            # small timeout so readline() won't block the GUI
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
            time.sleep(2)
            print("✅ Serial connected.")
        except serial.SerialException as e:
            print(f"⚠️ Could not open serial port: {e}")
            self.ser = None

    def send_servo_command(self, cmd):
        """Send a single command (letter A–Z or 'REL') to the ESP32."""
        if self.ser is None:
            print("⚠️ No serial connection, cannot send servo command.")
            return
        try:
            send_str = cmd + "\n"
            self.ser.write(send_str.encode('utf-8'))
            print(f"--> SENT TO ESP32: {cmd}")
        except serial.SerialException as e:
            print("Serial write error:", e)

    # ============== Continuous detection ============
    def check_continuous_detection(self, char, confidence):
        if confidence >= self.confidence_threshold:
            self.frame_history.append(char)
        else:
            self.frame_history.append(None)

        if len(self.frame_history) < self.required_continuous_frames:
            return False

        return all(x == char and x is not None for x in self.frame_history)

    # ============== Frame processing =================
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

        if results and results.multi_hand_landmarks:
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
                                # '0' = backspace
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
                                progress = len(
                                    [x for x in self.frame_history if x == current_prediction and x is not None]
                                )
                                detection_status = f"Detecting: {current_prediction} ({progress}/{self.required_continuous_frames})"
                        elif self.cooldown_counter > 0:
                            detection_status = f"Cooldown: {self.cooldown_counter} frames"
                        else:
                            detection_status = f"Low Confidence: {current_prediction}"

        # ---- UI text ----
        cv2.putText(frame_square, f"Words: {''.join(self.detected_words)}",
                    (20, H - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        status_color = (0, 255, 0) if "Detected:" in detection_status else (255, 255, 255)
        cv2.putText(frame_square, detection_status,
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

        settings_text = f"Settings: {self.required_continuous_frames} frames, {self.confidence_threshold*100:.0f}% confidence"
        cv2.putText(frame_square, settings_text,
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Updated instructions: BTN1 = Quit instead of REL
        instructions = "ESP Buttons: 32=Quit | 33=Voice+Servo | 25=Clear | 26=Speak | 'Q'=Quit"
        cv2.putText(frame_square, instructions,
                    (20, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        return frame_square[:H, :W]

    # ============== Drawing helpers =================
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
        cv2.rectangle(frame, (x, y), (x + width, y + height), (50, 50, 50), -1)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), (0, 255, 0), -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 255), 2)

    # ============== Backspace =================
    def handle_backspace(self):
        if self.detected_words:
            removed = self.detected_words.pop()
            print(f"⌫ Backspace removed: '{removed}'")
        else:
            print("⌫ Backspace but nothing to delete")

    # ============== Voice (Vosk) =================
    def listen_for_voice_word(self, timeout=4.0):
        """
        Listen with Vosk and return letters-only word (A–Z),
        truncated to MAX_VOICE_LETTERS letters.
        """
        if self.vosk_recognizer is None:
            print("⚠️ Vosk is not initialized.")
            return None

        print("🎤 Listening for voice word...")
        self.vosk_recognizer.Reset()

        q_audio = queue.Queue()

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(status, file=sys.stderr)
            q_audio.put(bytes(indata))

        block_size = int(SAMPLE_RATE * BLOCK_DURATION_MS / 1000)
        text_result = ""

        with sd.RawInputStream(samplerate=SAMPLE_RATE,
                               blocksize=block_size,
                               dtype='int16',
                               channels=1,
                               callback=audio_callback):
            start_time = time.time()
            while time.time() - start_time < timeout:
                remaining = timeout - (time.time() - start_time)
                if remaining <= 0:
                    break
                try:
                    data = q_audio.get(timeout=remaining)
                except queue.Empty:
                    break

                if self.vosk_recognizer.AcceptWaveform(data):
                    res = json.loads(self.vosk_recognizer.Result())
                    text = res.get("text", "").strip()
                    if text:
                        text_result = text
                        break

            if not text_result:
                res = json.loads(self.vosk_recognizer.FinalResult())
                text_result = res.get("text", "").strip()

        print(f"Vosk raw text: '{text_result}'")

        if not text_result:
            print("No voice detected.")
            return None

        letters = [ch.upper() for ch in text_result if ch.isalpha()]
        if not letters:
            print("No letters found in voice text.")
            return None

        word = ''.join(letters)

        # Enforce max length
        if len(word) > MAX_VOICE_LETTERS:
            print(f"Voice word too long ({len(word)} letters). Truncating to first {MAX_VOICE_LETTERS}.")
            word = word[:MAX_VOICE_LETTERS]

        print(f"Voice word letters: {word}")
        return word

    # ============== Servo + overlay ==============
    def play_word_on_servo_with_overlay(self, word):
        """
        2nd program:
        - full black background
        - show whole word in center
        - below that, show current letter
        - drive servo for each letter (A–Z) with LETTER_INTERVAL_SEC delay
        """
        word = word.strip().upper()
        if not word:
            print("No word to play on servo.")
            return

        if self.ser is None:
            print("⚠️ No serial connected, cannot drive servos.")
            return

        # Get frame size from camera, fall back if needed
        H = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 720)
        W = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1280)

        print(f"🎬 Playing word on servo: {word}")

        for ch in word:
            if not ch.isalpha():
                continue

            black = np.zeros((H, W, 3), dtype=np.uint8)

            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 3
            thickness = 4
            text_size, _ = cv2.getTextSize(word, font, scale, thickness)
            text_w, text_h = text_size
            x = (W - text_w) // 2
            y = (H + text_h) // 2

            # Draw the whole word in white
            cv2.putText(black, word, (x, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)

            # Show current letter in green below
            current_text = f"Letter: {ch}"
            cv2.putText(black, current_text, (x, y + 80), font, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow(self.window_name, black)
            cv2.waitKey(10)

            # Send letter to ESP32 (servo sequence)
            self.send_servo_command(ch)
            # Wait at least LETTER_INTERVAL_SEC seconds for this letter
            time.sleep(LETTER_INTERVAL_SEC)

        print("✅ Finished playing word on servo.")

    # ============== Serial button polling ==========
    def poll_serial_buttons(self):
        """
        Reads lines from ESP32:

        - 'BTN1' -> Quit program (escape)
        - 'BTN2' -> 2nd program: voice word + black screen + servo, then return to main
        - 'BTN3' -> clear current word
        - 'BTN4' -> speak current word
        """
        if self.ser is None:
            return
        try:
            while self.ser.in_waiting:
                line = self.ser.readline().decode(errors='ignore').strip()
                if not line:
                    break

                # Debug:
                # print("From ESP:", line)

                if line.startswith("BTN1"):
                    # Button 1: Quit the Python program
                    print("ESP Button1 -> Quit program")
                    self.running = False
                    return  # stop handling more lines this frame

                elif line.startswith("BTN2"):
                    # Button 2: 2nd program (voice word + servo + full-screen)
                    print("ESP Button2 -> Voice+Servo mode")
                    word = self.listen_for_voice_word(timeout=4.0)
                    if word:
                        # show in first program's word buffer
                        self.detected_words = list(word)
                        print(f"📥 New word from voice: {word}")
                        # run 2nd program (this will block for a while, then return)
                        self.play_word_on_servo_with_overlay(word)
                    else:
                        print("No valid word from voice.")

                elif line.startswith("BTN3"):
                    # Button 3: clear word
                    print("ESP Button3 -> clear word")
                    self.detected_words.clear()

                elif line.startswith("BTN4"):
                    # Button 4: speak word
                    if self.detected_words:
                        word = ''.join(self.detected_words)
                        print(f"ESP Button4 -> speak: {word}")
                        self.speak_text(word)
                    else:
                        print("ESP Button4 -> no word to speak")
        except serial.SerialException as e:
            print("Serial read error:", e)

    # ============== Main loop ======================
    def run(self):
        if self.cap is None or not self.cap.isOpened():
            print("❌ Camera is not initialized. Exiting.")
            return

        # Create full-screen window once
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Camera frame not received. Check camera index.")
                break

            frame = cv2.flip(frame, 1)

            # Handle incoming button messages from ESP
            self.poll_serial_buttons()
            if not self.running:
                break

            frame = self.process_frame(frame)
            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("Keyboard 'q' pressed -> Quit program")
                break
            elif key == 13:  # Enter => add space
                self.detected_words.append(' ')
                print("Added space from keyboard.")
            elif key == ord('c'):
                self.detected_words.clear()
            elif key == ord('s'):
                if self.detected_words:
                    self.speak_text(''.join(self.detected_words))

        self.cleanup()

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        if self.ser:
            self.ser.close()
            print("Serial closed.")
        print("Final words:", ''.join(self.detected_words))


if __name__ == "__main__":
    try:
        HandSignRecognizer().run()
    except Exception as e:
        print("Program crashed with error:", e)
        input("Press Enter to exit...")
