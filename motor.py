# motor.py
# Drive the vibration motor using a single GPIO pin.

import time
import RPi.GPIO as GPIO
from config import VIBRATOR_PIN, BUZZ_MS_SHORT, BUZZ_GAP_MS


def init_motor():
    GPIO.setup(VIBRATOR_PIN, GPIO.OUT, initial=GPIO.LOW)


def _pulse(ms: int):
    GPIO.output(VIBRATOR_PIN, GPIO.HIGH)
    time.sleep(ms / 1000.0)
    GPIO.output(VIBRATOR_PIN, GPIO.LOW)


def buzz(times: int = 1):
    """Buzz the motor 'times' times with a short gap."""
    times = max(1, int(times))
    for i in range(times):
        _pulse(BUZZ_MS_SHORT)
        if i < times - 1:
            time.sleep(BUZZ_GAP_MS / 1000.0)
