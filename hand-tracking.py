import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
 
# Initialize MediaPipe Hands (use one hand)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

# Start video capture
cap = cv2.VideoCapture(1)  #Can change this to 0 to change camera
time.sleep(2)  

click_active = False  
swipe_start_x = None  

def count_fingers(hand_landmarks):
    """Count the number of fingers extended based on the hand landmarks, excluding the thumb"""
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    count = 0

    # Count extended fingers
    for tip in finger_tips:
        # Check if the finger is fully extended
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y and \
           hand_landmarks.landmark[tip - 1].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    return count

def detect_swipe(current_x, previous_x):
    """Detect swipe direction based on the current and previous x positions of the index finger"""
    if previous_x is not None:
        delta_x = current_x - previous_x
        if delta_x < -80:  #Change this value for more or less sensitivity
            return "left"
        elif delta_x > 80:  #Change this value for more or less sensitivity
            return "right"
    return None

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  

        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get coordinates of the index finger tip
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x_index = int(index_finger_tip.x * frame.shape[1])
        y_index = int(index_finger_tip.y * frame.shape[0])

        # Store the current x position for swipe detection
        current_x = int(index_finger_tip.x * frame.shape[1])
        swipe_direction = detect_swipe(current_x, swipe_start_x)

        # Scale the coordinates to match screen size
        mouse_x = int(screen_width * (x_index / frame.shape[1]))
        mouse_y = int(screen_height * (y_index / frame.shape[0]))

        num_fingers = count_fingers(hand_landmarks)

        # Move the mouse cursor when the index finger is extended
        if num_fingers >= 1:
            pyautogui.moveTo(mouse_x, mouse_y)

        if num_fingers == 4:
            if not click_active:  # Activate click-and-hold
                pyautogui.mouseDown()  # Hold the mouse down
                click_active = True
        else:
            if click_active:  # Release the click-and-hold
                pyautogui.mouseUp()
                click_active = False


        if num_fingers == 2:  
            if swipe_direction == "left":
                print("Swipe Left Detected")
                cv2.putText(frame, 'Swipe Left', (x_index, y_index - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                pyautogui.hotkey('ctrl', 'right')  # Switch to next window
            elif swipe_direction == "right":
                print("Swipe Right Detected")
                cv2.putText(frame, 'Swipe Right', (x_index, y_index + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                pyautogui.hotkey('ctrl', 'left')  # Switch to previous window

            swipe_start_x = current_x
        else:
            swipe_start_x = None  

        # Display finger count and click state on the frame
        cv2.putText(frame, f'Fingers: {num_fingers}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        if click_active:
            cv2.putText(frame, 'Holding Mouse', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Mouse Not Held', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.rectangle(frame, (10, 150), (300, 250), (200, 200, 200), -1)  
        cv2.putText(frame, 'Gesture Control', (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        
        # Draw a bar representing finger count
        cv2.rectangle(frame, (20, 210), (20 + num_fingers * 40, 240), (0, 255, 0), -1)
        cv2.putText(frame, 'Finger Count', (150, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

        if swipe_direction == "left":
            cv2.arrowedLine(frame, (x_index, y_index), (x_index - 100, y_index), (255, 255, 0), 5)
        elif swipe_direction == "right":
            cv2.arrowedLine(frame, (x_index, y_index), (x_index + 100, y_index), (255, 255, 0), 5)

    cv2.imshow('Hand Tracking', frame)
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

