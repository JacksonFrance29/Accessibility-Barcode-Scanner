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

## How It Works

1. The device powers on and automatically runs the Python control script.
2. An ultrasonic sensor continuously measures the distance between the scanner and the product.
3. Audio feedback guides the user to move the scanner closer or farther to align the barcode using data from the ultrasonic sensor and webcam.
4. A USB webcam captures live video frames.
5. Computer vision logic scans each frame for a readable barcode.
6. Once a barcode is detected:
   - The vibration motor activates to confirm success
   - The barcode data is decoded
   - Product information is retrieved from a barcode database
   - Text-to-speech announces the product name and nutritional information
  








