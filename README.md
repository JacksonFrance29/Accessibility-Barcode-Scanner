# Accessibility Barcode Scanner (Raspberry Pi)
## Device Views

![Front View](assets/front.jpg)
![Back View](assets/back.jpg)

## Demo Video

A short demonstration of the scanner in use can be found here:
▶️ https://youtu.be/MzS8ri4AkV4

## Motivation
This project was designed to explore how embedded systems, sensors, and software can be combined to improve accessibility.
The goal was to create a portable, intuitive device that provides visually impaired users with greater independence in everyday shopping environments.

## Description
A handheld Raspberry Pi-based barcode scanning device designed to assist visually impaired users in everyday shopping environments through real-time auditory and tactile feedback. 
The device is completely portable, powered by a rechargeable battery pack, and runs a Python control script automatically upon startup.


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

## How It Works
1. The user powers the device on, and it automatically runs the Python control script.
2. A USB webcam captures live video frames.
3. An ultrasonic sensor continuously measures the distance between the scanner and the product.
4. Audio feedback through the Bluetooth speaker guides the user to move the scanner closer to or farther from the item to align the barcode using data from the ultrasonic sensor and webcam.
5. Computer vision logic scans each frame for a readable barcode.
6. Once a barcode is detected:
   - The vibration motor activates to confirm success
   - The barcode data is decoded
   - Product information is retrieved from a barcode database
   - Text-to-speech announces the product name and nutritional information
   - The device announces that it is ready to start the next scan
  







