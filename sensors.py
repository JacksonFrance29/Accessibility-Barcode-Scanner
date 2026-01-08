# sensors.py
# Ultrasonic distance measurement for HC-SR04-style sensor.

import time
import RPi.GPIO as GPIO
from config import US_TRIG_PIN, US_ECHO_PIN


def init_ultrasonic():
    GPIO.setup(US_TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(US_ECHO_PIN, GPIO.IN)


def get_distance_cm(timeout: float = 0.04):
    """Return distance in cm, or None if timeout."""
    # Settle
    GPIO.output(US_TRIG_PIN, GPIO.LOW)
    time.sleep(0.05)

    # 10µs trigger pulse
    GPIO.output(US_TRIG_PIN, GPIO.HIGH)
    time.sleep(10e-6)
    GPIO.output(US_TRIG_PIN, GPIO.LOW)

    start_wait = time.time()
    while GPIO.input(US_ECHO_PIN) == 0:
        if time.time() - start_wait > timeout:
            return None
    pulse_start = time.time()

    while GPIO.input(US_ECHO_PIN) == 1:
        if time.time() - pulse_start > timeout:
            return None
    pulse_end = time.time()

    duration = pulse_end - pulse_start
    # Speed of sound ~34300 cm/s
    distance = (duration * 34300) / 2.0
    return distance
