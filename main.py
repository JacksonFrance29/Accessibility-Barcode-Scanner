# main.py
# Orchestrates button, camera, ultrasonic, TTS, vibration, and product lookup.

import time
import threading
import RPi.GPIO as GPIO

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    BUTTON_PIN,
    SCAN_TIMEOUT_S,
    POST_DECODE_PAUSE_S,
)
from tts import speak
from motor import init_motor, buzz
from sensors import init_ultrasonic, get_distance_cm
from camera_scanner import BarcodeScanner, analyze_frame
from guidance import GuidanceState, guidance_message, maybe_say
from product_lookup import lookup_product
from chatgpt_client import generate_product_speech

# Global scan state
_scanning_lock = threading.Lock()
_scanning_flag = False


def button_pressed(channel):
    """Start a scan session if one isn't already running."""
    global _scanning_flag
    if _scanning_lock.acquire(blocking=False):
        try:
            if not _scanning_flag:
                _scanning_flag = True
                threading.Thread(target=run_scan_session, daemon=True).start()
        finally:
            _scanning_lock.release()


def run_scan_session():
    """Read camera frames, guide user, decode barcode, speak result."""
    global _scanning_flag

    speak("Starting scan. Sweep slowly.")
    scanner = BarcodeScanner(CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT)
    guidance_state = GuidanceState()
    have_announced_in_frame = False
    decoded_barcode = None
    start_time = time.time()

    try:
        while time.time() - start_time < SCAN_TIMEOUT_S:
            frame = scanner.read()
            if frame is None:
                continue

            analysis = analyze_frame(frame)
            distance_cm = get_distance_cm()

            msg = guidance_message(analysis, distance_cm)
            maybe_say(msg, guidance_state, speak)

            if analysis.had_any_barcode and not have_announced_in_frame:
                buzz(1)
                have_announced_in_frame = True

            if analysis.decoded:
                decoded_barcode = analysis.decoded
                buzz(2)
                speak("Barcode captured.")
                break

        if not decoded_barcode:
            speak("I could not read the barcode.")
            return

        info = lookup_product(decoded_barcode)
        speech = generate_product_speech(decoded_barcode, info)
        time.sleep(POST_DECODE_PAUSE_S)
        speak(speech)
    finally:
        scanner.release()
        _scanning_flag = False
        speak("Ready.")


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Button and peripherals
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    init_motor()
    init_ultrasonic()

    speak("Scanner ready. Press the trigger to begin.")

    # Polling loop for button
    prev = GPIO.input(BUTTON_PIN)
    try:
        while True:
            cur = GPIO.input(BUTTON_PIN)
            if prev == 1 and cur == 0:
                button_pressed(None)
            prev = cur
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
