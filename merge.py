import wmi
import speech_recognition as sr
import os
import webbrowser
import subprocess
import pyautogui  # For automating tasks like volume
import screen_brightness_control as sbc  # For brightness control
import cv2
import mediapipe as mp
import pygetwindow as gw
import time
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import numpy as np

recognizer = sr.Recognizer()

# Initialize Mediapipe hands and drawing utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Time tracking for click intervals
last_click_time = 0
click_interval = 0.4  # Time interval to detect double click

# Volume setup using pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get the volume range
vol_range = volume.GetVolumeRange()  # (-65.25, 0.0) in dB
min_vol = vol_range[0]
max_vol = vol_range[1]

def is_double_click():
    global last_click_time
    current_time = time.time()
    if current_time - last_click_time < click_interval:
        last_click_time = 0
        return True
    last_click_time = current_time
    return False

def focus_chrome():
    # Get the list of open windows
    chrome_windows = gw.getWindowsWithTitle("YouTube")  # Searches for a YouTube window
    if chrome_windows:
        chrome_windows[0].activate()  # Bring the first window with "YouTube" title into focus

def play_pause_video():
    focus_chrome()
    pyautogui.press('space')  # Simulates pressing spacebar

def skip_forward():
    focus_chrome()
    pyautogui.press('right')  # Simulates pressing right arrow

def skip_backward():
    focus_chrome()
    pyautogui.press('left')  # Simulates pressing left arrow

def set_volume(distance):
    # Map the distance to the volume range
    vol = np.interp(distance, [0.01, 0.15], [min_vol, max_vol])
    volume.SetMasterVolumeLevel(vol, None)

def capture_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text

def process_voice_command(text):
    text = text.lower()

    # Greeting and Goodbye
    if "hello" in text:
        print("Hello! How can I help you?")
    elif "goodbye" in text or "exit" in text:
        print("Goodbye! Have a great day!")
        return True

    # System control commands
    elif "shut down" in text:
        print("Shutting down the computer...")
        os.system("shutdown /s /t 1")
    elif "restart" in text:
        print("Restarting the computer...")
        os.system("shutdown /r /t 1")
    elif "lock the screen" in text:
        print("Locking the screen...")
        os.system("rundll32.exe user32.dll, LockWorkStation")

    # Volume Control
    elif "increase volume" in text:
        pyautogui.press("volumeup", presses=5)
        print("Increasing volume...")
    elif "decrease volume" in text:
        pyautogui.press("volumedown", presses=5)
        print("Decreasing volume...")
    elif "mute" in text:
        pyautogui.press("volumemute")
        print("Muting the sound...")
    elif "unmute" in text:
        pyautogui.press("volumemute")  # Pressing "mute" key again unmutes if it's currently muted
        print("Unmuting the sound...")

    # Brightness control using screen_brightness_control library
    elif "increase brightness" in text:
        current_brightness = sbc.get_brightness(display=0)  # Get brightness of the first display
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]  # Handle multiple monitors if necessary
        new_brightness = min(current_brightness + 10, 100)  # Cap brightness at 100%
        sbc.set_brightness(new_brightness)
        print(f"Increasing brightness to {new_brightness}%")
    elif "decrease brightness" in text:
        current_brightness = sbc.get_brightness(display=0)  # Get brightness of the first display
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]  # Handle multiple monitors if necessary
        new_brightness = max(current_brightness - 10, 0)  # Do not go below 0%
        sbc.set_brightness(new_brightness)
        print(f"Decreasing brightness to {new_brightness}%")

    # Web Browsing
    elif "open google" in text:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "search" in text:
        query = text.split("search for")[-1].strip()
        print(f"Searching for {query}...")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Application Control
    elif "open word" in text:
        print("Opening Microsoft Word...")
        os.startfile(r'C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE')  # Change path as per your installation
    elif "open chrome" in text:
        print("Opening Google Chrome...")
        os.startfile(r'C:/Program Files/Google/Chrome/Application/chrome.exe')
    elif "open excel" in text:
        print("Opening Microsoft Excel...")
        os.startfile(r'C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE')  # Change path as per your installation

    # Handle unrecognized commands
    else:
        print("I didn't understand that command. Please try again.")

    return False

def main():
    cap = cv2.VideoCapture(0)  # Initialize video capture for hand detection
    end_program = False
    while not end_program:
        audio = capture_voice_input()  # Capture voice command
        text = convert_voice_to_text(audio)  # Convert to text
        end_program = process_voice_command(text)  # Execute voice command

        success, img = cap.read()  # Read frame from the camera
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe processing
        results = hands.process(img_rgb)  # Process frame for hand tracking

        # If a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:  # Iterate over detected hands
                hand_label = 'Unknown'
                if results.multi_handedness:
                    for hand_handedness in results.multi_handedness:
                        hand_label = hand_handedness.classification[0].label  # 'Left' or 'Right'

                # Loop through the hand landmarks (e.g., thumb, index, etc.)
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)  # Get coordinates of the landmark
                    if id == 8:  # Tip of the index finger
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)  # Draw a circle at the index tip

                # Measure distance between thumb tip (id = 4) and index tip (id = 8)
                thumb_tip = handLms.landmark[4]
                index_tip = handLms.landmark[8]
                distance = hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)  # Euclidean distance

                # Set volume based on the distance between thumb and index finger
                set_volume(distance)

                # If the distance is below a certain threshold (fingers are close enough)
                if distance < 0.05:  # Adjust threshold based on your camera distance
                    if is_double_click():  # Check if it's a double click
                        if hand_label == 'Right':  # Double-click with right hand skips forward
                            skip_forward()
                        elif hand_label == 'Left':  # Double-click with left hand skips backward
                            skip_backward()
                    else:  # Single click toggles play/pause
                        play_pause_video()

                # Draw the hand landmarks
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

        # Display the video feed with detected hand landmarks
        cv2.imshow("Image", img)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
