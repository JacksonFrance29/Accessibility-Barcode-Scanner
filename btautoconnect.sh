#!/bin/bash
# Attempt to auto-connect a known Bluetooth speaker and set as default sink.

BT_DEVICE_MAC="BC:E2:77:29:78:C5"  # replace with your speaker MAC if needed

# Ensure bluetooth is up
rfkill unblock bluetooth
systemctl start bluetooth

# Try to connect a few times
for i in {1..5}; do
    echo -e "connect $BT_DEVICE_MAC\ntrust $BT_DEVICE_MAC\nquit" | bluetoothctl
    sleep 3
done

# Set default sink if present
if command -v pactl >/dev/null 2>&1; then
    SINK=$(pactl list short sinks | awk '/bluez_output/{print $1}' | head -n 1)
    if [ -n "$SINK" ]; then
        pactl set-default-sink "$SINK"
        pactl suspend-sink "$SINK" false
    fi
fi
