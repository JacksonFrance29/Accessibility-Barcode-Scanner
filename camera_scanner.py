# camera_scanner.py
# Webcam capture + barcode decoding using OpenCV and pyzbar.

from dataclasses import dataclass
from typing import Optional, Tuple
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, BLUR_THRESHOLD


@dataclass
class BarcodeFrameAnalysis:
    frame_w: int
    frame_h: int
    bbox_center: Optional[Tuple[int, int]]
    bbox_w: int
    blur_score: float
    had_any_barcode: bool
    decoded: Optional[str]


class BarcodeScanner:
    def __init__(self, camera_index: int, width: int, height: int):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        if not self.cap.isOpened():
            return None
        ok, frame = self.cap.read()
        if not ok:
            return None
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None


def analyze_frame(frame) -> BarcodeFrameAnalysis:
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur score via Laplacian (higher = sharper)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    codes = decode(gray)
    had_any = len(codes) > 0
    decoded = None
    bbox_center = None
    bbox_w = 0

    if codes:
        # Take the first barcode
        c = codes[0]
        decoded = c.data.decode("utf-8", errors="ignore") if c.data else None
        (x, y, bw, bh) = c.rect
        bbox_center = (x + bw // 2, y + bh // 2)
        bbox_w = bw

    return BarcodeFrameAnalysis(
        frame_w=w,
        frame_h=h,
        bbox_center=bbox_center,
        bbox_w=bbox_w,
        blur_score=float(blur_score),
        had_any_barcode=had_any,
        decoded=decoded,
    )
