import cv2
import pigpio
import time

# ========== SERVO SETUP ==========
SERVO_PIN = 18
STOP_PULSE = 1500        # Your calibrated stop pulse
PULSE_MIN = 500
PULSE_MAX = 2500

pi = pigpio.pi()
if not pi.connected:
    print("pigpio not running")
    exit()

def set_speed(speed_factor):
    if speed_factor > 1.0:
        speed_factor = 1.0
    elif speed_factor < -1.0:
        speed_factor = -1.0
    if speed_factor >= 0:
        pulse = STOP_PULSE + speed_factor * (PULSE_MAX - STOP_PULSE)
    else:
        pulse = STOP_PULSE + speed_factor * (STOP_PULSE - PULSE_MIN)
    pi.set_servo_pulsewidth(SERVO_PIN, int(pulse))

def stop_servo():
    pi.set_servo_pulsewidth(SERVO_PIN, STOP_PULSE)

stop_servo()
time.sleep(1)

# ========== CAMERA ==========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

# ========== FACE DETECTOR ==========
cascade_path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print("Error: Could not load cascade file")
    exit()

# ========== TRACKING PARAMETERS ==========
DEAD_ZONE = 100
Kp = 0.0002
MAX_SPEED = 0.05
UPDATE_INTERVAL = 0.2
NO_DETECTION_TIMEOUT = 2.0

last_update = time.time()
last_face_time = time.time()
smoothed_face_x = None
scale = 640 / 320   # = 2.0

# ========== WINDOW SETUP ==========
WINDOW_NAME = "Face Tracking (640x480)"
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
fullscreen = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Create a smaller frame for detection
        small_frame = cv2.resize(frame, (320, 240))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25,25))

        speed_cmd = 0.0
        frame_center_x = frame.shape[1] // 2   # 320

        if len(faces) > 0:
            last_face_time = time.time()
            (x_small, y_small, w_small, h_small) = max(faces, key=lambda f: f[2]*f[3])
            x = int(x_small * scale)
            w = int(w_small * scale)
            face_center_x = x + w//2

            if smoothed_face_x is None:
                smoothed_face_x = face_center_x
            else:
                smoothed_face_x = 0.7 * smoothed_face_x + 0.3 * face_center_x

            y = int(y_small * scale)
            h = int(h_small * scale)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.circle(frame, (int(smoothed_face_x), frame.shape[0]//2), 5, (0,0,255), -1)

            error = smoothed_face_x - frame_center_x
            print(f"Error: {error:.0f} pixels")

            if abs(error) > DEAD_ZONE:
                speed_cmd = -Kp * error
                if speed_cmd > MAX_SPEED:
                    speed_cmd = MAX_SPEED
                elif speed_cmd < -MAX_SPEED:
                    speed_cmd = -MAX_SPEED
            else:
                speed_cmd = 0.0
        else:
            print("No face detected")
            smoothed_face_x = None
            if time.time() - last_face_time > NO_DETECTION_TIMEOUT:
                speed_cmd = 0.0

        now = time.time()
        if now - last_update >= UPDATE_INTERVAL:
            set_speed(speed_cmd)
            last_update = now

        cv2.imshow(WINDOW_NAME, frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            fullscreen = not fullscreen
            if fullscreen:
                cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            else:
                cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

except KeyboardInterrupt:
    pass

stop_servo()
pi.stop()
cap.release()
cv2.destroyAllWindows()
