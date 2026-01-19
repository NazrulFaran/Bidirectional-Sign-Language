#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVO_MIN 150
#define SERVO_MAX 600

// ---- Button pins (change if you want) ----
const int BUTTON1_PIN = 32; // voice word + servo (BTN1)
const int BUTTON2_PIN = 33; // REL / home (BTN2)
const int BUTTON3_PIN = 25; // clear word in Python (BTN3)
const int BUTTON4_PIN = 26; // speak word in Python (BTN4)

// ---------- HELPER FUNCTIONS ----------

uint16_t angleToPulse(int angle) {
  angle = constrain(angle, 0, 180);
  return map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
}

void setServoAngle(uint8_t channel, int angle) {
  if (channel > 15) return;           // we only have 16 channels (0–15)
  angle = constrain(angle, 0, 180);
  pwm.setPWM(channel, 0, angleToPulse(angle));
}

// ---------- YOUR CUSTOM FUNCTIONS ----------
void releasePosition() {
  // Example initial angles – CHANGE these to your needs:
  setServoAngle(0, 0); 
  setServoAngle(1, 150); 
  setServoAngle(2, 150); 
  setServoAngle(3, 0); 
  setServoAngle(4, 150); 
  setServoAngle(5, 150); 
  setServoAngle(6, 150); 
  setServoAngle(7, 0); 
  setServoAngle(8, 0); 
  setServoAngle(9, 150); 
  setServoAngle(10, 0); 
  setServoAngle(11, 0); 
  setServoAngle(12, 120); 
  setServoAngle(13, 70); 


  Serial.println("Release / home position set.");
}

// Sequence for command 'A'
void runSequenceA() {
  Serial.println("Running sequence A...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);
  setServoAngle(12, 140);
  setServoAngle(13, 90);
  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 30);
  setServoAngle(10, 110);
  delay(200);
  setServoAngle(13, 0);
  setServoAngle(12, 125);

  delay(3000);


  setServoAngle(13, 90);
  setServoAngle(12, 140);
  delay(200);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);
  setServoAngle(13, 70);
  setServoAngle(12, 120);


  Serial.println("Sequence A done.");
}

// Sequence for command 'B'
void runSequenceB() {
  Serial.println("Running sequence B...");

  setServoAngle(12, 50);
  delay(100);
  setServoAngle(13, 0);

  delay(3000);

  setServoAngle(13, 70);
  delay(200);
  setServoAngle(12, 120);


  Serial.println("Sequence B done.");
}

// Sequence for command 'C'
void runSequenceC() {
  Serial.println("Running sequence C...");

  setServoAngle(2, 95);
  setServoAngle(5, 90);
  setServoAngle(8, 65);
  setServoAngle(11, 60);
  // delay(500);
  delay(200);
  setServoAngle(13, 40);
  setServoAngle(12, 110);

  delay(3000);


  setServoAngle(13, 70);
  setServoAngle(12, 120);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);


  Serial.println("Sequence C done.");
}

// Sequence for command 'D'
void runSequenceD() {
  Serial.println("Running sequence D...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  delay(100);
  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 110);

  delay(3000);


  setServoAngle(12, 140);
  delay(100);
  setServoAngle(13, 80);
  delay(100);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(12, 120);
  setServoAngle(13, 70);

  Serial.println("Sequence D done.");
}


// Sequence for command 'E'
void runSequenceE() {
  Serial.println("Running sequence E...");

  setServoAngle(12, 0);
  setServoAngle(13, 0);
  delay(200);
  setServoAngle(13, 0);
  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);
  delay(400);
  setServoAngle(0, 40);
  setServoAngle(1, 110);
  setServoAngle(3, 45);
  setServoAngle(4, 105);
  setServoAngle(6, 110);
  setServoAngle(7, 45);
  setServoAngle(9, 105);
  setServoAngle(10, 40);

  delay(3000);

  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(400);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);
  delay(200);
  setServoAngle(12, 120);
  setServoAngle(13, 70);


  Serial.println("Sequence e done.");
}

// Sequence for command 'F'
void runSequenceF() {
  Serial.println("Running sequence F...");

  
  setServoAngle(11, 90);
  setServoAngle(13, 90);
  delay(500);
  setServoAngle(9, 30);
  setServoAngle(10, 110);
  delay(200);
  setServoAngle(13, 40);
  setServoAngle(12, 95);

  delay(3000);


  setServoAngle(13, 90);
  setServoAngle(12, 120);
  delay(200);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(11, 0);


  Serial.println("Sequence F done.");
}

// Sequence for command 'G'
void runSequenceG() {
  Serial.println("Running sequence G...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(13, 100);
  setServoAngle(12, 140);
  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(10, 35);
  delay(200);
  setServoAngle(13, 0);


  delay(3000);


  setServoAngle(13, 100);
  setServoAngle(12, 140);
  delay(200); 
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(12, 120);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);

  Serial.println("Sequence G done.");
}

// Sequence for command 'H'
void runSequenceH() {
  Serial.println("Running sequence H...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(13, 100);
  setServoAngle(12, 140);
  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(7, 30);
  setServoAngle(10, 35);
  delay(200);
  setServoAngle(13, 0);


  delay(3000);


  setServoAngle(13, 100);
  setServoAngle(12, 140);
  delay(200);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(7, 0);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(12, 120);
  setServoAngle(2, 150);
  setServoAngle(5, 150);

  Serial.println("Sequence H done.");
}

// Sequence for command 'I'
void runSequenceI() {
  Serial.println("Running sequence I...");

  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);
  setServoAngle(13, 90);
  delay(500);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 30);
  setServoAngle(10, 110);
  delay(200);
  setServoAngle(13, 0);
  setServoAngle(12, 85);

  delay(3000);


  setServoAngle(13, 90);
  setServoAngle(12, 120);
  delay(200);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);


  Serial.println("Sequence I done.");
}

// Sequence for command 'J'
void runSequenceJ() {
  Serial.println("Running sequence J...");

  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);
  setServoAngle(13, 90);
  delay(500);
  setServoAngle(0, 40);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 30);
  setServoAngle(10, 110);
  delay(200);
  setServoAngle(13, 0);
  setServoAngle(12, 85);

  delay(3000);


  setServoAngle(13, 90);
  setServoAngle(12, 120);
  delay(200);
  setServoAngle(0, 0);
  // setServoAngle(1, 135);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  // delay(200);
  // setServoAngle(1, 150);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);


  Serial.println("Sequence J done.");
}

// Sequence for command 'K'
void runSequenceK() {
  Serial.println("Running sequence K...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(13, 100);
  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  delay(200);
  setServoAngle(13, 0);


  delay(3000);


  setServoAngle(13, 100);
  delay(200);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(2, 150);
  setServoAngle(5, 150);

  Serial.println("Sequence K done.");
}

// Sequence for command 'L'
void runSequenceL() {
  Serial.println("Running sequence L...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(13, 130);
  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(12, 150);

  delay(3000);

  setServoAngle(12, 120);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);

  Serial.println("Sequence L done.");
}

// Sequence for command 'M'
void runSequenceM() {
  Serial.println("Running sequence M...");

  setServoAngle(2, 70);
  delay(200);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  delay(100);
  setServoAngle(13, 0);
  setServoAngle(12, 30);
  delay(300);
  setServoAngle(5, 90);
  setServoAngle(8, 70);
  setServoAngle(11, 60);
  delay(400);
  setServoAngle(3, 90);
  setServoAngle(4, 60);
  setServoAngle(6, 50);
  setServoAngle(7, 90);
  setServoAngle(9, 60);
  setServoAngle(10, 80);

  delay(3000);

  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(400);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);
  delay(200);
  setServoAngle(13, 70);
  setServoAngle(12, 120);


  Serial.println("Sequence M done.");
}


// Sequence for command 'N'
void runSequenceN() {
  Serial.println("Running sequence N...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  delay(200);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  delay(100);
  setServoAngle(13, 0);
  setServoAngle(12, 50);
  delay(300);
  setServoAngle(8, 70);
  setServoAngle(11, 60);
  delay(400);
  setServoAngle(6, 50);
  setServoAngle(7, 90);
  setServoAngle(9, 60);
  setServoAngle(10, 80);

  delay(3000);

  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(400);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);
  delay(200);
  setServoAngle(13, 70);
  setServoAngle(12, 120);


  Serial.println("Sequence N done.");
}

// Sequence for command 'O'
void runSequenceO() {
  Serial.println("Running sequence O...");

  setServoAngle(2, 95);
  setServoAngle(5, 90);
  setServoAngle(8, 65);
  setServoAngle(11, 60);
  delay(200);
  setServoAngle(13, 60);
  setServoAngle(12, 90);
  delay(400);
  setServoAngle(0, 35);
  setServoAngle(1, 115);
  setServoAngle(3, 45);
  setServoAngle(4, 105);
  setServoAngle(6, 100);
  setServoAngle(7, 50);
  setServoAngle(9, 105);
  setServoAngle(10, 45);


  delay(3000);

  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(400);
  setServoAngle(13, 70);
  setServoAngle(12, 120);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);


  Serial.println("Sequence O done.");
}

// Sequence for command 'P'
void runSequenceP() {
  Serial.println("Running sequence P...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 115);
  setServoAngle(10, 35);
  delay(100);
  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 110);

  delay(3000);


  setServoAngle(12, 140);
  delay(100);
  setServoAngle(13, 80);
  delay(100);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(12, 120);
  setServoAngle(13, 70);

  Serial.println("Sequence P done.");
}


// Sequence for command 'Q'
void runSequenceQ() {
  Serial.println("Running sequence Q...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 115);
  setServoAngle(10, 35);
  delay(100);
  setServoAngle(13, 50);
  delay(100);
  setServoAngle(12, 150);

  delay(3000);


  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(12, 120);
  setServoAngle(13, 70);

  Serial.println("Sequence Q done.");
}


// Sequence for command 'R'
void runSequenceR() {
  Serial.println("Running sequence R...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(9, 130);
  setServoAngle(10, 40);
  delay(200);
  setServoAngle(6, 130);
  delay(100);
  setServoAngle(8, 30);
  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 95);

  delay(3000);


  setServoAngle(12, 120);
  delay(100);
  setServoAngle(13, 70);
  setServoAngle(8, 0);
  delay(100);
  setServoAngle(6, 150);
  delay(200);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);

  Serial.println("Sequence R done.");
}

// Sequence for command 'S'
void runSequenceS() {
  Serial.println("Running sequence S...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);
  setServoAngle(13, 90);
  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 30);
  setServoAngle(10, 110);
  delay(200);
  setServoAngle(13, 0);
  setServoAngle(12, 85);

  delay(3000);


  setServoAngle(13, 90);
  setServoAngle(12, 120);
  delay(200);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(13, 70);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);


  Serial.println("Sequence S done.");
}

// Sequence for command 'T'
void runSequenceT() {
  Serial.println("Running sequence T...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  delay(200);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  delay(100);
  setServoAngle(13, 0);
  setServoAngle(12, 85);
  delay(300);
  setServoAngle(11, 60);
  delay(400);
  setServoAngle(9, 90);
  setServoAngle(10, 50);

  delay(3000);

  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(200);
  setServoAngle(13, 70);
  setServoAngle(12, 120);
  delay(200);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  delay(400);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);



  Serial.println("Sequence T done.");
}

// Sequence for command 'U'
void runSequenceU() {
  Serial.println("Running sequence U...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 130);
  setServoAngle(9, 125);
  delay(100);
  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 95);

  delay(3000);


  setServoAngle(12, 120);
  delay(100);
  setServoAngle(13, 70);
  delay(100);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(9, 150);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);

  Serial.println("Sequence U done.");
}

// Sequence for command 'V'
void runSequenceV() {
  Serial.println("Running sequence V...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  delay(100);
  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 95);

  delay(3000);


  setServoAngle(12, 120);
  delay(100);
  setServoAngle(13, 70);
  delay(100);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);

  Serial.println("Sequence V done.");
}

// Sequence for command 'W'
void runSequenceW() {
  Serial.println("Running sequence W...");

  setServoAngle(2, 70);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 120);
  setServoAngle(1, 50);
  delay(100);
  setServoAngle(13, 30);
  delay(100);
  setServoAngle(12, 60);

  delay(3000);


  setServoAngle(12, 120);
  delay(100);
  setServoAngle(13, 70);
  setServoAngle(1, 150);
  setServoAngle(0, 0);
  delay(500);
  setServoAngle(2, 150);

  Serial.println("Sequence W done.");
}

// Sequence for command 'X'
void runSequenceX() {
  Serial.println("Running sequence X...");

  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 0);
  delay(200);
  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 130);


  delay(3000);


  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);
  delay(200);
  setServoAngle(13, 70);
  delay(100);
  setServoAngle(12, 120);
  
  Serial.println("Sequence X done.");
}

// Sequence for command 'Y'
void runSequenceY() {
  Serial.println("Running sequence Y...");

  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(11, 90);
  delay(500);
  setServoAngle(0, 40);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 30);
  setServoAngle(10, 110);
  setServoAngle(12, 150);
  setServoAngle(13, 80);


  delay(3000);


  setServoAngle(0, 0);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(11, 0);
  setServoAngle(12, 120);
  setServoAngle(13, 70);

  Serial.println("Sequence Y done.");
}

// Sequence for command 'Z'
void runSequenceZ() {
  Serial.println("Running sequence Z...");

  setServoAngle(2, 70);
  setServoAngle(5, 60);
  setServoAngle(8, 100);
  setServoAngle(12, 140);
  setServoAngle(13, 80);

  delay(500);
  setServoAngle(0, 110);
  setServoAngle(1, 50);
  setServoAngle(3, 120);
  setServoAngle(4, 30);
  setServoAngle(6, 20);
  setServoAngle(7, 120);
  setServoAngle(9, 100);
  setServoAngle(10, 50);
  delay(100);
  setServoAngle(13, 40);
  delay(100);
  setServoAngle(12, 110);

  delay(3000);


  setServoAngle(12, 140);
  delay(100);
  setServoAngle(13, 80);
  delay(100);
  setServoAngle(0, 0);
  setServoAngle(1, 150);
  setServoAngle(3, 0);
  setServoAngle(4, 150);
  setServoAngle(6, 150);
  setServoAngle(7, 0);
  setServoAngle(9, 150);
  setServoAngle(10, 0);
  delay(500);
  setServoAngle(2, 150);
  setServoAngle(5, 150);
  setServoAngle(8, 0);
  setServoAngle(12, 120);
  setServoAngle(13, 70);

  Serial.println("Sequence Z done.");
}


// ---------- BUTTON HANDLING ----------

void checkButtons() {
  static int last1 = HIGH, last2 = HIGH, last3 = HIGH, last4 = HIGH;

  int b1 = digitalRead(BUTTON1_PIN);
  int b2 = digitalRead(BUTTON2_PIN);
  int b3 = digitalRead(BUTTON3_PIN);
  int b4 = digitalRead(BUTTON4_PIN);

  // Edge detection: HIGH -> LOW = pressed
  if (last1 == HIGH && b1 == LOW) {
    Serial.println("BTN1");  // voice word + servo
  }
  if (last2 == HIGH && b2 == LOW) {
    Serial.println("BTN2");  // REL
  }
  if (last3 == HIGH && b3 == LOW) {
    Serial.println("BTN3");  // clear word
  }
  if (last4 == HIGH && b4 == LOW) {
    Serial.println("BTN4");  // speak word
  }

  last1 = b1;
  last2 = b2;
  last3 = b3;
  last4 = b4;
}

// ---------- SETUP & LOOP ----------

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);  // for ESP32 – SDA=21, SCL=22

  // Button pins
  pinMode(BUTTON1_PIN, INPUT_PULLUP);
  pinMode(BUTTON2_PIN, INPUT_PULLUP);
  pinMode(BUTTON3_PIN, INPUT_PULLUP);
  pinMode(BUTTON4_PIN, INPUT_PULLUP);

  pwm.begin();
  pwm.setPWMFreq(50);  // 50 Hz for servos

  // Move all servos to initial "release" position once at power-on
  releasePosition();

  Serial.println("READY");
  Serial.println("Commands:");
  Serial.println("  A..Z  -> run sequences A..Z");
  Serial.println("  REL   -> release/home position");
  Serial.println("  RET   -> release/home position (alias)");
  Serial.println("  channel angle  (example: 5 90)");
}

void loop() {
  // Check hardware buttons every loop
  checkButtons();

  // Handle incoming serial commands from Python
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() == 0) return;

    if (input.equalsIgnoreCase("A")) {
      runSequenceA();
      return;
    } else if (input.equalsIgnoreCase("B")) {
      runSequenceB();
      return;
    } else if (input.equalsIgnoreCase("C")) {
      runSequenceC();
      return;
    } else if (input.equalsIgnoreCase("D")) {
      runSequenceD();
      return;
    } else if (input.equalsIgnoreCase("E")) {
      runSequenceE();
      return;
    } else if (input.equalsIgnoreCase("F")) {
      runSequenceF();
      return;
    } else if (input.equalsIgnoreCase("G")) {
      runSequenceG();
      return;
    } else if (input.equalsIgnoreCase("H")) {
      runSequenceH();
      return;
    } else if (input.equalsIgnoreCase("I")) {
      runSequenceI();
      return;
    } else if (input.equalsIgnoreCase("J")) {
      runSequenceJ();
      return;
    } else if (input.equalsIgnoreCase("K")) {
      runSequenceK();
      return;
    } else if (input.equalsIgnoreCase("L")) {
      runSequenceL();
      return;
    } else if (input.equalsIgnoreCase("M")) {
      runSequenceM();
      return;
    } else if (input.equalsIgnoreCase("N")) {
      runSequenceN();
      return;
    } else if (input.equalsIgnoreCase("O")) {
      runSequenceO();
      return;
    } else if (input.equalsIgnoreCase("P")) {
      runSequenceP();
      return;
    } else if (input.equalsIgnoreCase("Q")) {
      runSequenceQ();
      return;
    } else if (input.equalsIgnoreCase("R")) {
      runSequenceR();
      return;
    } else if (input.equalsIgnoreCase("S")) {
      runSequenceS();
      return;
    } else if (input.equalsIgnoreCase("T")) {
      runSequenceT();
      return;
    } else if (input.equalsIgnoreCase("U")) {
      runSequenceU();
      return;
    } else if (input.equalsIgnoreCase("V")) {
      runSequenceV();
      return;
    } else if (input.equalsIgnoreCase("W")) {
      runSequenceW();
      return;
    } else if (input.equalsIgnoreCase("X")) {
      runSequenceX();
      return;
    } else if (input.equalsIgnoreCase("Y")) {
      runSequenceY();
      return;
    } else if (input.equalsIgnoreCase("Z")) {
      runSequenceZ();
      return;
    } else if (input.equalsIgnoreCase("REL") || input.equalsIgnoreCase("RET")) {
      releasePosition();
      return;
    } else {
      // Try to interpret as: "channel angle"
      int channel, angle;
      if (sscanf(input.c_str(), "%d %d", &channel, &angle) == 2) {
        if (channel >= 0 && channel <= 15 && angle >= 0 && angle <= 180) {
          setServoAngle(channel, angle);
          Serial.print("Channel ");
          Serial.print(channel);
          Serial.print(" -> ");
          Serial.print(angle);
          Serial.println(" degrees");
        } else {
          Serial.println("Invalid channel or angle range.");
        }
      } else {
        Serial.print("Unknown command: ");
        Serial.println(input);
      }
    }
  }
}
