import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time
import os
from math import hypot
import numpy as np

# Initialize Mediapipe hands and drawing utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Time tracking for click intervals
last_click_time = 0
click_interval = 0.4  # Time interval to detect double click

# Define smoothing parameters for mouse movement
smooth_factor = 7
prev_x, prev_y = 0, 0

def is_double_click():
    global last_click_time
    current_time = time.time()
    if current_time - last_click_time < click_interval:
        last_click_time = 0
        return True
    last_click_time = current_time
    return False

def focus_chrome():
    chrome_windows = gw.getWindowsWithTitle("YouTube")
    if chrome_windows:
        chrome_windows[0].activate()

def play_pause_video():
    focus_chrome()
    pyautogui.press('space')

def skip_forward():
    focus_chrome()
    pyautogui.press('right')

def skip_backward():
    focus_chrome()
    pyautogui.press('left')

def open_folder():
    os.startfile(os.path.expanduser("D:/Downloads"))

# Start video capture from webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()  # Read frame from the camera
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe processing
    results = hands.process(img_rgb)  # Process frame for hand tracking

    # If a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            hand_label = 'Unknown'
            if results.multi_handedness:
                for hand_handedness in results.multi_handedness:
                    hand_label = hand_handedness.classification[0].label  # 'Left' or 'Right'

            # Get the hand's index finger and thumb positions for distance calculation
            thumb_tip = handLms.landmark[4]
            index_tip = handLms.landmark[8]
            h, w, c = img.shape

            # Get cursor control coordinates
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            distance = hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

            # Screen dimensions
            screen_w, screen_h = pyautogui.size()

            # Smoothing the cursor movement
            cur_x = np.interp(index_tip.x * w, [0, w], [0, screen_w])
            cur_y = np.interp(index_tip.y * h, [0, h], [0, screen_h])
            smooth_x = prev_x + (cur_x - prev_x) / smooth_factor
            smooth_y = prev_y + (cur_y - prev_y) / smooth_factor

            # Move the mouse to the smoothed coordinates
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y

            # Click action for distance threshold (~15 cm)
            if distance < 0.05:
                if is_double_click():
                    if hand_label == 'Right':
                        skip_forward()
                    elif hand_label == 'Left':
                        skip_backward()
                else:
                    play_pause_video()  # Single click for play/pause
            elif distance < 0.15:
                pyautogui.click()
                # Uncomment to open folder
                # open_folder()

            # Draw landmarks
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Display the video feed with hand tracking
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the program
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()











# import cv2
# import mediapipe as mp
# import pyautogui
# import pygetwindow as gw
# import time
# from math import hypot
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from comtypes import CLSCTX_ALL
# import numpy as np
 
# # Initialize Mediapipe hands and drawing utilities
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_draw = mp.solutions.drawing_utils

# # Time tracking for click intervals
# last_click_time = 0
# click_interval = 0.4  # Time interval to detect double click

# # Volume setup using pycaw
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = interface.QueryInterface(IAudioEndpointVolume)

# # Get the volume range
# vol_range = volume.GetVolumeRange()  # (-65.25, 0.0) in dB
# min_vol = vol_range[0]
# max_vol = vol_range[1]

# def is_double_click():
#     global last_click_time
#     current_time = time.time()
#     if current_time - last_click_time < click_interval:
#         last_click_time = 0
#         return True
#     last_click_time = current_time
#     return False

# def focus_chrome():
#     # Get the list of open windows
#     chrome_windows = gw.getWindowsWithTitle("YouTube")  # Searches for a YouTube window
#     if chrome_windows:
#         chrome_windows[0].activate()  # Bring the first window with "YouTube" title into focus

# def play_pause_video():
#     focus_chrome()
#     pyautogui.press('space')  # Simulates pressing spacebar

# def skip_forward():
#     focus_chrome()
#     pyautogui.press('right')  # Simulates pressing right arrow

# def skip_backward():
#     focus_chrome()
#     pyautogui.press('left')  # Simulates pressing left arrow

# def set_volume(distance):
#     # Map the distance to the volume range
#     vol = np.interp(distance, [0.01, 0.15], [min_vol, max_vol])
#     volume.SetMasterVolumeLevel(vol, None)

# # Start video capture from webcam
# cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()  # Read frame from the camera
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe processing
#     results = hands.process(img_rgb)  # Process frame for hand tracking

#     # If a hand is detected
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:  # Iterate over detected hands

#             # Determine if the hand is left or right
#             hand_label = 'Unknown'
#             if results.multi_handedness:
#                 for hand_handedness in results.multi_handedness:
#                     hand_label = hand_handedness.classification[0].label  # 'Left' or 'Right'

#             # Loop through the hand landmarks (e.g., thumb, index, etc.)
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)  # Get coordinates of the landmark
#                 if id == 8:  # Tip of the index finger
#                     cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)  # Draw a circle at the index tip

#             # Measure distance between thumb tip (id = 4) and index tip (id = 8)
#             thumb_tip = handLms.landmark[4]
#             index_tip = handLms.landmark[8]
#             distance = hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)  # Euclidean distance

#             # Set volume based on the distance between thumb and index finger
#             set_volume(distance)

#             # If the distance is below a certain threshold (fingers are close enough)
#             if distance < 0.05:  # Adjust threshold based on your camera distance
#                 if is_double_click():  # Check if it's a double click
#                     if hand_label == 'Right':  # Double-click with right hand skips forward
#                         skip_forward()
#                     elif hand_label == 'Left':  # Double-click with left hand skips backward
#                         skip_backward()
#                 else:  # Single click toggles play/pause
#                     play_pause_video()

#             # Draw the hand landmarks
#             mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

#     # Display the video feed with hand tracking
#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the program
#         break

# # Release the camera and close windows
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp
# import pyautogui
# import pygetwindow as gw  # To bring Chrome window into focus
# import time
# from math import hypot

# # Initialize Mediapipe hands and drawing utilities
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_draw = mp.solutions.drawing_utils

# # Time tracking for click intervals
# last_click_time = 0
# click_interval = 0.4  # Time interval to detect double click

# def is_double_click():
#     global last_click_time
#     current_time = time.time()
#     if current_time - last_click_time < click_interval:
#         last_click_time = 0
#         return True
#     last_click_time = current_time
#     return False

# def focus_chrome():
#     # Get the list of open windows
#     chrome_windows = gw.getWindowsWithTitle("YouTube")  # Searches for a YouTube window
#     if chrome_windows:
#         chrome_windows[0].activate()  # Bring the first window with "YouTube" title into focus

# def play_pause_video():
#     focus_chrome()
#     pyautogui.press('space')  # Simulates pressing spacebar

# def skip_forward():
#     focus_chrome()
#     pyautogui.press('right')  # Simulates pressing right arrow

# def skip_backward():
#     focus_chrome()
#     pyautogui.press('left')  # Simulates pressing left arrow

# # Start video capture from webcam
# cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()  # Read frame from the camera
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe processing
#     results = hands.process(img_rgb)  # Process frame for hand tracking

#     # If a hand is detected
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:  # Iterate over detected hands

#             # Determine if the hand is left or right
#             hand_label = 'Unknown'
#             if results.multi_handedness:
#                 for hand_handedness in results.multi_handedness:
#                     hand_label = hand_handedness.classification[0].label  # 'Left' or 'Right'

#             # Loop through the hand landmarks (e.g., thumb, index, etc.)
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)  # Get coordinates of the landmark
#                 if id == 8:  # Tip of the index finger
#                     cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)  # Draw a circle at the index tip

#             # Measure distance between thumb tip (id = 4) and index tip (id = 8)
#             thumb_tip = handLms.landmark[4]
#             index_tip = handLms.landmark[8]
#             distance = hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)  # Euclidean distance

#             # If the distance is below a certain threshold (fingers are close enough)
#             if distance < 0.05:  # Adjust threshold based on your camera distance
#                 if is_double_click():  # Check if it's a double click
#                     if hand_label == 'Right':  # Double-click with right hand skips forward
#                         skip_forward()
#                     elif hand_label == 'Left':  # Double-click with left hand skips backward
#                         skip_backward()
#                 else:  # Single click toggles play/pause
#                     play_pause_video()

#             # Draw the hand landmarks
#             mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

#     # Display the video feed with hand tracking
#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the program
#         break

# # Release the camera and close windows
# cap.release()
# cv2.destroyAllWindows()



# import cv2
# import mediapipe as mp
# import pyautogui
# import time
# from math import hypot

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_draw = mp.solutions.drawing_utils

# last_click_time = 0
# click_interval = 0.4

# def is_double_click():
#     global last_click_time
#     current_time = time.time()
#     if current_time - last_click_time < click_interval:
#         last_click_time = 0
#         return True
#     last_click_time = current_time
#     return False

# def play_pause_video():
#     pyautogui.press('space')

# def skip_forward():
#     pyautogui.press('right')

# def skip_backward():
#     pyautogui.press('left')

# cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             hand_label = 'Unknown'
#             if results.multi_handedness:
#                 for hand_handedness in results.multi_handedness:
#                     hand_label = hand_handedness.classification[0].label

#             # Drawing landmarks and connections
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 if id == 8:  # Tip of the index finger
#                     cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

#             thumb_tip = handLms.landmark[4]
#             index_tip = handLms.landmark[8]
#             distance = hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

#             if distance < 0.05:  # Adjust threshold
#                 if is_double_click():
#                     if hand_label == 'Right':
#                         skip_forward()
#                     elif hand_label == 'Left':
#                         skip_backward()
#                 else:
#                     play_pause_video()

#             mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
