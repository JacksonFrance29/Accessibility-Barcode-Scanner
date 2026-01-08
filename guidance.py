# guidance.py
# Turn camera + ultrasonic info into human-friendly guidance sentences.

import time
from dataclasses import dataclass
from typing import Optional, Tuple
from config import (
    CENTER_TOLERANCE_PX,
    MIN_BARCODE_WIDTH_PX,
    BLUR_THRESHOLD,
    GUIDANCE_COOLDOWN_S,
    MIN_DISTANCE_CM,
    MAX_DISTANCE_CM,
)
from camera_scanner import BarcodeFrameAnalysis


@dataclass
class GuidanceState:
    last_message: Optional[str] = None
    last_spoken_time: float = 0.0


def _centering_phrase(frame_w: int, bbox_center: Tuple[int, int]) -> Optional[str]:
    cx, cy = bbox_center
    center_x = frame_w // 2
    dx = cx - center_x

    if abs(dx) <= CENTER_TOLERANCE_PX:
        return "Horizontally centered."
    if dx < 0:
        return "Move slightly to the left."
    else:
        return "Move slightly to the right."


def _distance_phrase(distance_cm: Optional[float]) -> Optional[str]:
    if distance_cm is None:
        return None
    # Clamp
    d = max(0.0, min(float(distance_cm), 999.0))

    if d < MIN_DISTANCE_CM:
        delta = int(round(MIN_DISTANCE_CM - d))
        return f"Move back about {delta} centimeters."
    if d > MAX_DISTANCE_CM:
        delta = int(round(d - MAX_DISTANCE_CM))
        return f"Move forward about {delta} centimeters."
    return "Distance is good."


def guidance_message(analysis: BarcodeFrameAnalysis, distance_cm: Optional[float]) -> str:
    # No barcode at all
    if not analysis.had_any_barcode:
        if analysis.blur_score < BLUR_THRESHOLD:
            return "I can't see the barcode. Hold steady for a moment."
        return "Sweep slowly until I see the barcode."

    parts = []

    if analysis.bbox_center is not None:
        center_msg = _centering_phrase(analysis.frame_w, analysis.bbox_center)
        if center_msg and "centered" not in center_msg.lower():
            parts.append(center_msg)

    dist_msg = _distance_phrase(distance_cm)
    if dist_msg and "good" not in dist_msg.lower():
        parts.append(dist_msg)

    # If nothing specific, encourage stability
    if not parts:
        if analysis.blur_score < BLUR_THRESHOLD:
            return "Hold very still, I'm trying to read the barcode."
        return "Hold that position, reading the barcode."

    return " ".join(parts)


def maybe_say(msg: str, state: GuidanceState, speak_func):
    now = time.time()
    if not msg:
        return
    if state.last_message == msg and now - state.last_spoken_time < GUIDANCE_COOLDOWN_S:
        return
    state.last_message = msg
    state.last_spoken_time = now
    speak_func(msg)
