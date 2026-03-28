import pigpio
import time

SERVO_PIN = 18
pi = pigpio.pi()
if not pi.connected:
    exit()

print("Sweeping up...")
for pw in range(500, 1480, 5):
    pi.set_servo_pulsewidth(SERVO_PIN, pw)
    print(f"Pulse: {pw} µs")
    time.sleep(0.2)

print("\nSweeping down...")
for pw in range(1480, 500, -5):
    pi.set_servo_pulsewidth(SERVO_PIN, pw)
    print(f"Pulse: {pw} µs")
    time.sleep(0.2)

pi.set_servo_pulsewidth(SERVO_PIN, 0)
pi.stop()
