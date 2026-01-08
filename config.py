# config.py
# Central configuration for GPIO pins, camera, TTS, and timing.

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# GPIO pins (BCM numbering)
BUTTON_PIN = 17        # trigger button (with pull-up)
VIBRATOR_PIN = 27      # vibration motor via transistor
US_TRIG_PIN = 23       # ultrasonic trigger
US_ECHO_PIN = 24       # ultrasonic echo

# Guidance parameters
CENTER_TOLERANCE_PX = 80
MIN_BARCODE_WIDTH_PX = 320
BLUR_THRESHOLD = 120.0
GUIDANCE_COOLDOWN_S = 1.5

# Distance ranges (cm)
MIN_DISTANCE_CM = 10
MAX_DISTANCE_CM = 60

# Vibration timing (milliseconds)
BUZZ_MS_SHORT = 120
BUZZ_GAP_MS = 120

# OpenAI / OpenFoodFacts
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = "gpt-4o-mini"
OPENFOODFACTS_BASE = "https://world.openfoodfacts.org/api/v2/product"

# Text-to-speech
TTS_ENGINE = "espeak-ng"
TTS_WPM = "170"
TTS_VOICE = "en-us"

# Scan timing
SCAN_TIMEOUT_S = 30
POST_DECODE_PAUSE_S = 1.5
