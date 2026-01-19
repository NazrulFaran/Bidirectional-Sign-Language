# Bidirectional Sign Language 🤟🔁🗣️

**Bidirectional Sign Language** is an interactive system that converts:

- **Hand signs → Speech** (via camera + hand pose model + TTS)
- **Voice → Robotic hand gestures** (via Vosk speech recognition + ESP32 + servos)

It uses a camera and deep learning on the PC side, and an ESP32 + PCA9685 + multiple servos + physical buttons on the hardware side.

---

## ✨ Features

- **Sign → Speech**
  - Real-time hand sign recognition using MediaPipe Hands + a custom TensorFlow model.
  - Each detected letter is spoken using Windows TTS (`winspeech`).
  - Builds up a word on-screen (with support for backspace and spacing).
  
- **Voice → Robotic Hand (Servo sequences)**
  - Press a physical button on the ESP32.
  - PC listens with a microphone using Vosk ASR (offline speech recognition).
  - Extracts **only letters (A–Z)**, truncates to **max 6 letters**.
  - Full-screen black display shows the **whole word** and the **current letter**.
  - Sends each letter one-by-one to ESP32, with **8 seconds delay per letter**.
  - ESP32 runs a custom servo sequence for each letter (A–Z, REL, etc.).

- **Hardware buttons on ESP32**
  - 4 buttons, all wired as `GPIO ↔ button ↔ GND` with `INPUT_PULLUP`.
  - Button mappings:
    - **BTN1 (GPIO 32)** → Quit the Python app (same as pressing `Q`).
    - **BTN2 (GPIO 33)** → Voice→Servo mode (record word and play on servos).
    - **BTN3 (GPIO 25)** → Clear current word in the Python app.
    - **BTN4 (GPIO 26)** → Speak currently detected word via TTS.

---

## 🧱 System Architecture

### PC Side (Python)

- **HandSignRecognizer** main class
  - Loads `improved_hand_model.h5` and `label_encoder.pickle`.
  - Uses **MediaPipe Hands** to extract 21 landmarks and normalize them.
  - Sends landmark vectors into the TensorFlow model to classify gesture (A–Z, `0` for backspace).
  - Uses **OpenCV** to show live video, bounding boxes, confidence bars, and the current word.
  - Uses **winspeech** to speak detected letters or full word.
  - Manages full-screen mode and UI overlays.

- **Vosk voice recognition**
  - Uses `vosk-model-small-en-us-0.15` (offline model, path configured via `VOSK_MODEL_PATH`).
  - Listens for a short window (e.g. 4 seconds) after the Voice+Servo button is pressed.
  - Converts recognized text to uppercase letters only, discards non-letters.
  - Truncates word to `MAX_VOICE_LETTERS = 6`.

- **Serial communication**
  - `pyserial` opens `COM7` at `115200` baud (configurable).
  - Receives button codes (`BTN1`, `BTN2`, `BTN3`, `BTN4`) from ESP32.
  - Sends single-character commands `A`–`Z` or `REL` to ESP32, one per servo gesture.

### ESP32 Side

- Hardware:
  - **ESP32** (with I2C pins 21 (SDA), 22 (SCL)).
  - **PCA9685** 16-channel servo driver (I2C address `0x40`).
  - Up to 14+ servos connected to PCA9685 channels (0–13).
  - 4 push buttons connected:
    - `GPIO32` (BTN1)
    - `GPIO33` (BTN2)
    - `GPIO25` (BTN3)
    - `GPIO26` (BTN4)
    - Each wired as: `GPIO ↔ button ↔ GND`.

- Firmware:
  - Uses `Adafruit_PWMServoDriver` to control servos via PWM.
  - Each letter `A`–`Z` has a dedicated `runSequenceX()` function.
  - `REL` and/or an initial `releasePosition()` sets base/idle posture.
  - A `checkButtons()` function:
    - Reads button states.
    - On `HIGH→LOW` transitions, prints `BTN1`, `BTN2`, `BTN3`, `BTN4` over Serial.

> The PC reads these lines and maps them to actions (Quit, Voice+Servo, Clear, Speak).

---

## 🛠️ Requirements

### Hardware

- ESP32 development board.
- PCA9685 16-channel servo driver.
- Multiple servos (e.g. 14 standard servos).
- 4 push buttons.
- Wires, breadboard or PCB.
- Stable 5V power supply for servos (with common ground to ESP32).
- USB cable from ESP32 to PC.
- Webcam.
- Microphone (for voice input).

### Software

- **OS:** Windows (required for `winspeech`).
- **Python:** 3.8+ (tested in Anaconda environment).
- **Libraries:** (see `requirements.txt`)
  - `opencv-python`
  - `mediapipe`
  - `numpy`
  - `tensorflow`
  - `winspeech`
  - `vosk`
  - `sounddevice`
  - `pyserial`

---

## 🚀 Getting Started

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/Bidirectional-Sign-Language.git
cd Bidirectional-Sign-Language
