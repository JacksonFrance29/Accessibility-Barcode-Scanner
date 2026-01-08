# tts.py
# Simple wrapper around espeak-ng for TTS on Raspberry Pi.

import subprocess
import threading
from queue import Queue, Empty
from config import TTS_ENGINE, TTS_WPM, TTS_VOICE

_queue: "Queue[str]" = Queue()
_worker_started = False
_lock = threading.Lock()


def _tts_worker():
    while True:
        text = _queue.get()
        if text is None:
            break
        try:
            # Use espeak-ng directly
            subprocess.run(
                [
                    TTS_ENGINE,
                    "-s",
                    TTS_WPM,
                    "-v",
                    TTS_VOICE,
                    text,
                ],
                check=False,
            )
        except Exception:
            # Fail silently; this is best-effort
            pass
        finally:
            _queue.task_done()


def _ensure_worker():
    global _worker_started
    with _lock:
        if not _worker_started:
            t = threading.Thread(target=_tts_worker, daemon=True)
            t.start()
            _worker_started = True


def speak(text: str):
    """Enqueue text to be spoken asynchronously."""
    if not text:
        return
    _ensure_worker()
    _queue.put(str(text))
