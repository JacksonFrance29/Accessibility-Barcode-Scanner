# Accessibility Barcode Scanner (Raspberry Pi)

A handheld Raspberry Pi-based barcode scanning device designed to assist visually impaired users in shopping environments through real-time auditory and tactile feedback. 
The scanner utilizes an ultrasonic sensor and a webcam to guide the user in positioning the device to capture the barcode.
Auditory instructions are provided through a Bluetooth speaker to get the barcode into frame, and tactile feedback is provided through the vibration motor once the barcode is captured.
The device then uses text-to-speech to describe the item and provides the item's nutritional information retrieved from a barcode database.
The device is completely portable, powered by a rechargeable battery pack, and runs a Python script automatically upon startup.


## Tech Stack

**Hardware**
- Raspberry Pi
- USB webcam
- Ultrasonic distance sensor
- Bluetooth Speaker
- Vibration motor
- Tactile button
- Breadboard, wiring
- 3D printed enclosure
- Portable battery

**Software**
- Python
- GPIO + sensor integration
- Text-to-speech
- Barcode recognition/computer vision
