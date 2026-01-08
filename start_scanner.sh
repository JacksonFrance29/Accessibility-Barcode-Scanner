#!/bin/bash
# Run the scanner app from boot (called from rc.local)

cd /home/pi/scanner || exit 1
/bin/bash -lc "source venv/bin/activate && python main.py > /home/pi/scanner/log.txt 2>&1 &"
