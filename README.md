# DEMO

![DEMO](demo.gif) 

# Hand Gesture Recognition & Control

This project implements real-time hand tracking and gesture recognition using Computer Vision and Machine Learning techniques. By utilizing a webcam, the project allows users to control the mouse cursor and perform actions like selecting text or swiping between windows, enhancing human-computer interaction through intuitive hand gestures.

## Features

- **Move Mouse**: Control the mouse cursor by simply moving your index finger across the screen.
- **Swipe Between Windows**: Use two-finger gestures to swipe left or right between open windows.
- **Select Text (Mouse Hold)**: Hold the mouse button down by extending four fingers and drag to select text.

## How It Works

The project uses OpenCV for capturing video from a webcam and MediaPipe for detecting hand landmarks and gestures. With deep learning models from MediaPipe, it processes hand movements and converts them into mouse and keyboard actions using `pyautogui`.

## MediaPipe

[MediaPipe](https://mediapipe.dev/) is an open-source framework developed by Google that uses machine learning (specifically deep learning) for real-time tracking and processing of human hands. It provides high accuracy and speed by detecting 21 different hand landmarks, allowing our system to recognize gestures such as swipes, clicks, and more. This enables us to map hand movements to computer commands, creating an efficient and natural interaction interface.

## Technologies Used

- **OpenCV**: To capture and process video frames in real-time.
- **MediaPipe**: For accurate and efficient hand detection and gesture recognition.
- **PyAutoGUI**: To control the mouse and perform keyboard actions based on recognized gestures.
- **NumPy**: To handle array operations and transformations within the code.

## Setup Instructions

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Omarharradi/Hand-Gesture-Mouse-Control.git

2. Install the required dependencies by using the requirements.txt file:
   ```bash
   pip install -r requirements.txt

3. Run the Python script and start controlling your computer using hand gestures:
   ```bash
   python3 hand_tracking.py
